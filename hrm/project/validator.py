from django.core.validators import RegexValidator


zip_validate = RegexValidator(r'^[0-9]*$', 'Please enter valid zip code.')
phone_validate = RegexValidator(r'^\s*\d{5}-\d{5}\s*$',
                                'Please enter valid phone number. Phone number is allowed in following '
                                  'pattern 12345-67890.')