from django.shortcuts import render
from blogs.models import Blogs
from django.db.models import Sum #สำหรับใช้งาน sum หายอดวิวรวม
from django.contrib.auth.decorators import login_required #ใช้งานการ login
from django.contrib.auth.models import auth
# Create your views here.

@login_required(login_url="member") #จะเรียกใช้ function panel ต้อง log in ก่อน 

def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views")) #การหายอด view รวม
    return render(request,"backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total})