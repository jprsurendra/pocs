from .serializers import DepartmentSerializer, RegistrationDataSerializer, HRRegistrationSerailizer, EmployeUpdateSerializer
from rest_framework import viewsets, mixins
from .models import User, Department
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from project.custom_permission import IsHREmployee

class CustomAuthToken(ObtainAuthToken):
    """
    custom auth token
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        token, created = Token.objects.get_or_create(user=user)
        user = User.objects.get(pk=user.id)
        print(user)
        response = {
            "data": {
                'token': token.key,
                'user_id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        }
        response['status'] = {"status": "User logged in successfully."}
        return Response(response)


class DepartmentApi(viewsets.ModelViewSet):
    '''
    Department Api for CRUD operation
    '''
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = PageNumberPagination


class EmployeeDataApi(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """
    employee_address: we have to pass address objects in list like:
    [{"address": "Gali no. 4", "country": "India","city": "karnal","zip": 12345},
    {"address": "casd","country": "India","city": "karnal","zip": 12345}]
    :return
    """
    queryset = User.objects.filter(is_employee=True, is_active=True)
    serializer_class = RegistrationDataSerializer
    permission_classes = [IsAuthenticated, IsHREmployee]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        serializer = RegistrationDataSerializer
        if self.action == 'update':
            serializer = EmployeUpdateSerializer
        return serializer

    def create(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            user = serialized.create(validated_data=serialized.data)
            serialized = self.serializer_class(user)
            response = serialized.data
            response['success_message_head'] = "Successfully Created"
            return Response(response, status=201)


class HRRegisterApi(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    '''HR Api to perform create and listing of HR'''
    queryset = User.objects.filter(is_hr=True, is_active=True)
    serializer_class = HRRegistrationSerailizer
    pagination_class = PageNumberPagination