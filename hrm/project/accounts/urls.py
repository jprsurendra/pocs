from django.urls import path, include
from rest_framework import routers
from accounts import api as v1_api


router = routers.DefaultRouter()
router.register(r'department', v1_api.DepartmentApi)
router.register(r'employee', v1_api.EmployeeDataApi)
router.register(r'hr/registration', v1_api.HRRegisterApi)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/login/', v1_api.CustomAuthToken.as_view()),

]