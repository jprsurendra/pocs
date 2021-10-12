from .models import User, EmployeeAddress, Department
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class DepartmentSerializer(serializers.ModelSerializer):
    '''
    Department serializer for CRUD operation
    '''
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = '__all__'


class HRRegistrationSerailizer(serializers.ModelSerializer):
    '''HR registration Serailizer'''
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'confirm_password'},
        error_messages={
            "blank": "Confirm password cannot be empty.",
            "min_length": "Confirm_password too short.",
        },
    )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'password and confirm password does not match.'})
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_hr=True
        )
        user.set_password(self.context['request'].data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']


class RegistrationDataSerializer(HRRegistrationSerailizer):
    """Employee Registration Serializer for creating employee with multiple addresses need to pass address
    objects in list"""
    employee_address = serializers.ListSerializer(child=EmployeeAddressSerializer(), required=False)
    department = DepartmentSerializer()

    def get_employee_address(self, obj):
        print(obj.employee_address.all())
        return obj.employee_address.all()

    def create(self, validated_data):
        department = validated_data.get('department')
        if validated_data['department']:
            department = get_object_or_404(Department, pk=validated_data.get('department'))
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            is_employee=True,
            age=validated_data.get('age'),
            phone=validated_data.get('phone'),
            department=department,
        )
        user.set_password(self.context['request'].data['password'])
        user.save()
        employee_address = validated_data.pop('employee_address')
        for address in employee_address:
            EmployeeAddress(
                employee=user,
                address=address.get('address'),
                country=address.get('country'),
                city=address.get('city'),
                zip=address.get('zip'),
            ).save()
        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'age', 'phone', 'department',
                  'employee_address', 'password', 'confirm_password']


class EmployeUpdateSerializer(serializers.ModelSerializer):
    '''Update employee data serializer only some fields but address can be added umlimited here'''
    employee_address = serializers.ListSerializer(child=EmployeeAddressSerializer(), required=False)

    def get_employee_address(self, obj):
        return obj.employee_address.all()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'age', 'phone', 'department',
                  'employee_address']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.department = validated_data.get('department', instance.department)
        instance.save()

        employee_address = validated_data.pop('employee_address')
        for address in employee_address:
            EmployeeAddress(
                employee=instance,
                address=address.get('address'),
                country=address.get('country'),
                city=address.get('city'),
                zip=address.get('zip'),
            ).save()
        return instance