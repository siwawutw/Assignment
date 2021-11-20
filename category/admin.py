from django.contrib import admin
from .models import Category

#เพิ่มหน้าจัดการ Category ให้ admin
# Register your models here.
admin.site.register(Category)