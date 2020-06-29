from django.contrib import admin

# Register your models here.
from empapp import models

admin.site.register(models.Employee)