#สำหรับควบคุมการทำงานในแอป blogs
from django.urls import path
from .views import panel,displayForm,insertData,deleteData

urlpatterns = [
    path('',panel,name="panel"),
    path('displayForm',displayForm,name="displayForm"),
    path('insertData',insertData,name="insertData"),
    path('deleteData/<int:id>',deleteData,name='deleteData'),
]
