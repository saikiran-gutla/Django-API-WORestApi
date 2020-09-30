from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.generic import View

from .models import Employee
from .mixins import HttpResponseMixin, SerializerMixin
from .forms import EmployeeForm

# Create your views here.
from .utils import is_valid_json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeView(HttpResponseMixin, SerializerMixin, View):
    def get_object_by_id(self, emp_id):
        try:
            emp = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            emp = None
        return emp

    def get(self, request, *args, **kwargs):
        data = request.body
        if not is_valid_json(data):
            data = json.dumps({'msg': 'The data is not in valid json format', 'data': data})
            return self.render_to_http_response(data, status=400)
        p_data = json.loads(data)
        print(f"PDATA : {p_data}")
        employee_id = p_data.get('id', None)
        print(f"EMPLOYEE ID :{employee_id}")
        if employee_id is not None:
            emp_details = self.get_object_by_id(employee_id)
            # try:
            #     emp_details = self.get_object_by_id(employee_id)
            # except Employee.DoesNotExist:
            #     json_data = json.dumps({'msg': 'Employee does not exist with the provided id'})
            #     return self.render_to_http_response(json_data=json_data, status=404)
            # else:
            if emp_details is not None:
                json_data = self.serialize_data(data=emp_details, fields=('e_no', 'e_name'))
                return self.render_to_http_response(json_data, status=None)
            else:
                json_data = json.dumps({'msg': 'Employee does not exist with the provided id'})
                return self.render_to_http_response(json_data=json_data, status=404)
        qs = Employee.objects.all()
        print(f"QS : {qs}")
        json_data = self.serialize_data(queryset=qs)
        return self.render_to_http_response(json_data, status=200)

    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.body
        print(f"Body Data : {data}")
        if not is_valid_json(data):
            data = json.dumps({'msg': 'The data is not in valid json format', 'data': data})
            return self.render_to_http_response(data, status=400)
        emp_data = json.loads(data)
        form = EmployeeForm(emp_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=302)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({'msg': 'Data stored to database'})
            return self.render_to_http_response(json_data, status=None)

    def put(self, request, *args, **kwargs):
        e_data = request.body
        if not is_valid_json(e_data):
            data = json.dumps({'msg': 'The data is not in valid json format', 'data': e_data})
            return self.render_to_http_response(data, status=400)

        emp_json_data = json.loads(e_data)
        e_id = emp_json_data.get('id', None)
        if e_id is not None:
            emp_details = self.get_object_by_id(emp_id=e_id)
            print(f"Returned Employee Details : {emp_details}")
            if emp_details is None:
                data = json.dumps({'msg': 'User does not Exits for provided ID'})
                return self.render_to_http_response(data, status=302)
            data = request.body
            if not is_valid_json(data):
                data = json.dumps({'msg': 'The data is not in valid json format', 'data': data})
                return self.render_to_http_response(data, status=400)
            provided_data = json.loads(data)
            original_data = {
                'e_no': emp_details.e_no,
                'e_name': emp_details.e_name,
                'e_sal': emp_details.e_sal,
                'e_addr': emp_details.e_addr
            }
            original_data.update(provided_data)
            form = EmployeeForm(original_data, instance=emp_details)
            if form.errors:
                json_data = json.dumps(form.errors)
                return self.render_to_http_response(json_data, status=302)
            if form.is_valid():
                form.save(commit=True)
                json_data = json.dumps({'msg': 'Data Updated in database'})
                return self.render_to_http_response(json_data, status=None)
        else:
            data = json.dumps({'msg': 'User does not Exits for provided ID'})
            return self.render_to_http_response(data, status=302)

    def delete(self, request, *args, **kwargs):
        e_data = request.body
        if not is_valid_json(e_data):
            data = json.dumps({'msg': 'The data is not in valid json format', 'data': e_data})
            return self.render_to_http_response(data, status=400)
        employee_data = json.loads(e_data)
        employee_id = employee_data.get('id', None)
        if employee_id is not None:
            emp_details = self.get_object_by_id(emp_id=employee_id)
            if emp_details is None:
                data = json.dumps({'msg': 'User does not Exits for provided ID'})
                return self.render_to_http_response(data, status=302)
            response, obj = emp_details.delete()
            if response == 1:
                data = json.dumps({'msg': 'User Deleted'})
                return self.render_to_http_response(data, status=200)
            data = json.dumps({'msg': 'Some Error occurred while removing User'})
            return self.render_to_http_response(data, status=500)
        else:
            json_data = json.dumps({'msg': 'User does not exist with provided UserID'})
            return self.render_to_http_response(json_data, status=301)
