from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.generic import View
from .models import Employee
from .mixins import HttpResponseMixin, SerializerMixin
from django.core.serializers import serialize
from .forms import EmployeeForm

# Create your views here.
from .utils import is_valid_json


class EmployeeView(HttpResponseMixin, SerializerMixin, View):
    def get_object_by_id(self, emp_id):
        try:
            emp = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            emp = None
        return emp

    def get(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=5)
        except Employee.DoesNotExist:
            json_data = json.dumps({'msg': 'Employee does not exist with the provided id'})
            return self.render_to_http_response(json_data=json_data, status=404)
        else:
            json_data = self.serialize_data(data=employee, fields=('e_no', 'e_name'))
            return self.render_to_http_response(json_data, status=None)

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
        emp_details = self.get_object_by_id(emp_id=12)
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

    def delete(self, request, *args, **kwargs):
        emp_details = self.get_object_by_id(emp_id=9)
        if emp_details is None:
            data = json.dumps({'msg': 'User does not Exits for provided ID'})
            return self.render_to_http_response(data, status=302)
        response, obj = emp_details.delete()
        if response == 1:
            data = json.dumps({'msg': 'User Deleted'})
            return self.render_to_http_response(data, status=200)
        data = json.dumps({'msg': 'Some Error occurred while removing User'})
        return self.render_to_http_response(data, status=500)