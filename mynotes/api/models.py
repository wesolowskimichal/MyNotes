from datetime import timezone
import uuid
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator

class Contact(models.Model):
    user_from = models.ForeignKey('User', related_name='from_contacts', on_delete=models.CASCADE)
    user_to = models.ForeignKey('User', related_name='to_contacts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user_from', 'user_to'),)
    
    def __str__(self) -> str:
        return f'{self.user_from} is connected to {self.user_to}'

class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=False, blank=False, max_length=150)
    sender = models.ForeignKey('User', related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey('User', related_name='received_requests', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        with transaction.atomic():
            contact = Contact.objects.create(user_from=self.sender, user_to=self.receiver)
            self.delete()
        return contact

    def deny(self):
        self.delete()

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    def upload_to(self, filename) -> str:
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
   
    def __str__(self) -> str:
        return self.username

class Group(models.Model):
    def __str__(self) -> str:
        return self.name
    
    def upload_to(self, filename) -> str:
        return f'groups/{self.id}/{filename}'
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(help_text='Required. Group\'s name', unique=False, blank=False, max_length=50, validators=[
        MinLengthValidator(1)
    ])
    image = models.ImageField(upload_to=upload_to, default='/defaults/group-default.png')
    owners = models.ManyToManyField(User, related_name='owned_note_groups', blank=True)
    members = models.ManyToManyField(User, related_name='note_groups', blank=True)


class Note(models.Model):
    def __str__(self) -> str:
        return ''
    
    def upload_to(seelf, filename) -> str:
        return f'notes/'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(help_text='Required. Note\'s title', unique=False, blank=False, max_length=50, validators=[MinLengthValidator(1)])
    htmlCode = models.TextField(help_text='HTML content of the note. Includes CodeBlock.', default='')
    nativeCode = models.TextField(help_text='Native content of the note. Includes CodeBlock.', default='')
    owners = models.ManyToManyField(User, related_name='owned_notes', blank=True)
    members = models.ManyToManyField(User, related_name='notes', blank=True)