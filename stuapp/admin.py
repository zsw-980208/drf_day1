from django.contrib import admin

# Register your models here.
from stuapp import models

admin.site.register(models.Student)