from django.contrib import admin
from .models import Operation, Balance


admin.site.register(Balance)
admin.site.register(Operation)