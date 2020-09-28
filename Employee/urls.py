from django.urls import path
from .views import EmployeeView

urlpatterns = [
    path(r'api/', EmployeeView.as_view()),
]
