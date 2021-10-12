from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from validator import zip_validate, phone_validate
# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Department(models.Model):
    name = models.CharField('Department Name', max_length=30, unique=True)


class User(AbstractUser):
    """Custom User model."""

    username = None
    email = models.EmailField('email address', unique=True, validators=[EmailValidator(message="Please enter a valid email address.")] )
    first_name = models.CharField('first name', max_length=30, blank=True, null=True )
    last_name = models.CharField('last name', max_length=30, blank=True, null=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, default=None, validators=[phone_validate])
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=False, help_text='Designates whether this user '
                                                               'should be treated as Employee in case True.')
    is_hr = models.BooleanField(default=False, help_text='Designates whether this user '
                                                               'should be treated as HR in case True.')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


class EmployeeAddress(models.Model):
    employee = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='employee_address')
    address = models.CharField('Address', max_length=100, blank=True, null=True)
    country = models.CharField('Country', max_length=50, blank=True, null=True)
    city = models.CharField('City', max_length=50, blank=True, null=True)
    zip = models.CharField('zip Code', max_length=5, blank=True, null=True, validators=[zip_validate])

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)