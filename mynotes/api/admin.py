from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(ContactRequest)
admin.site.register(Group)
admin.site.register(Note)