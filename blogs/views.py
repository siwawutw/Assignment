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
    #บทความยอดนิยม (เรียงลำดับจาก view มากไปน้อย)
    popular = Blogs.objects.all().order_by('-views')[:3]
    #บทความแนะนำ
    suggestion  = Blogs.objects.all().order_by('views')[:3] 
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
        
    return render(request,"frontend/index.html",{'categories':categories,'blogs':blogPerpage,'lastest':lastest,'popular':popular,'suggestion':suggestion})
    
def blogDetail(request,id):
    singleblog = Blogs.objects.get(id=id) #เรียกเข้าไปดูรายละเอียดบทความ
    singleblog.views = singleblog.views+1 #การเพิ่มยอดวิวเมื่อเข้าไปอ่านบทความ
    singleblog.save() #การเพิ่มยอดวิวเมื่อเข้าไปอ่านบทความ
    categories = Category.objects.all() #ดึงข้อมูล categgory ทั้งหมด
    popular = Blogs.objects.all().order_by('-views')[:3]    #บทความยอดนิยม
    suggestion  = Blogs.objects.all().order_by('views')[:3]  #บทความแนะนำ
    return render(request,"frontend/blogDetail.html",{"blog":singleblog,"categories":categories,"popular":popular,"suggestion":suggestion})

def searchCategory(request,cat_id):
    blogs = Blogs.objects.filter(category_id=cat_id)
    popular = Blogs.objects.all().order_by('-views')[:3]
    #บทความแนะนำ
    suggestion  = Blogs.objects.all().order_by('views')[:3] 
    categories = Category.objects.all() #ดึงข้อมูล categgory ทั้งหมด
    categoryName = Category.objects.get(id=cat_id)
    return render(request, "frontend/searchCategory.html",{"blogs":blogs,"popular":popular,"suggestion":suggestion,"categories":categories,"categoryName":categoryName })
    
def searchWriter(request,writer):
    
    blogs = Blogs.objects.filter(writer = writer)
    popular = Blogs.objects.all().order_by('-views')[:3] 
    suggestion  = Blogs.objects.all().order_by('views')[:3] #บทความแนะนำ
    categories = Category.objects.all() #ดึงข้อมูล categgory ทั้งหมด
    return render(request, "frontend/searchWriter.html",{"blogs":blogs,"popular":popular,"suggestion":suggestion,"categories":categories,"writer":writer})

def aboutus(request):
    popular = Blogs.objects.all().order_by('-views')[:3]
    #บทความแนะนำ
    suggestion  = Blogs.objects.all().order_by('views')[:3] 
    return render(request, 'frontend/aboutus.html',{'popular':popular,'suggestion':suggestion})