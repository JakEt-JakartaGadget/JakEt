from django.contrib import admin

# Register your models here.

from .models import Discussion, Reply

admin.site.register(Discussion)
admin.site.register(Reply)