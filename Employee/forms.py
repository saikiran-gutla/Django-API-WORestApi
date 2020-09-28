from django import forms
from Employee.models import Employee


class EmployeeForm(forms.ModelForm):
    def clean_e_sal(self):
        salary = self.cleaned_data['e_sal']
        print(f"SALARY : {salary}")
        if salary < 10000:
            raise forms.ValidationError('The minimum salary should be 10,000')
        return salary

    class Meta:
        model = Employee
        fields = "__all__"
