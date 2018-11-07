from django.contrib import admin

# Register your models here.

from .models import Orders

admin.site.register(Orders)
