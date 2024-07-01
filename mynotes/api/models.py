import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator

class User(AbstractUser):
    def __str__(self) -> str:
        return self.username
    
    def upload_to(self, filename):
        return f'users/{self.id}/{filename}'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_to, default='/defaults/user-default.png')
    first_name = models.CharField(help_text='Required. First name', unique=False, blank=False, max_length=150, validators=[
        MinLengthValidator(2),
        RegexValidator(
            regex='^[a-zA-Z]+$',
            message='First name must contain only letters',
            code='invalid_first_name'
        )
    ])
    last_name = models.CharField(help_text='Required. Last name', unique=False, blank=False, max_length=150, validators=[
        MinLengthValidator(2),
        RegexValidator(
            regex='^[a-zA-Z]+$',
            message='First name must contain only letters',
            code='invalid_first_name'
        )
    ])
    email = models.EmailField(help_text='Requirerd. Email address', unique=True)