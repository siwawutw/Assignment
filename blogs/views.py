from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category #เรียกใช้ฐานข้อมูลจาก app category 
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage
# Create your views here.
def index(request):
    categories = Category.objects.all() #ดึงข้อมูล categgory ทั้งหมด
    blogs=Blogs.objects.all()
    lastest = Blogs.objects.all().order_by('-pk')[:2]#ดึงข้อมูล บทความทั้งหมด โดยเรียงลำดับจาก id ที่มากสุดขึ้นก่อน โดยดึงแค่ 2 ตัว

    #pagination
    paginator = Paginator(blogs,3) #แบ่งให้แสดง 3 บทความต่อหนึ่งหน้า
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    
    try : 
        blogPerpage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages)
        
    return render(request,"frontend/index.html",{'categories':categories,'blogs':blogPerpage,'lastest':lastest})
    
def blogDetail(request,id):
    singleblog = Blogs.objects.get(id=id)
    return render(request,"frontend/blogDetail.html",{"blog":singleblog})