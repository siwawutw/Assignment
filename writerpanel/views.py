from django.shortcuts import redirect, render
from blogs.models import Blogs
from django.db.models import Sum #สำหรับใช้งาน sum หายอดวิวรวม
from django.contrib.auth.decorators import login_required #ใช้งานการ login
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage #ทำงานกับ file รูปที่ส่งมาในการสร้างบทความ
from django.contrib import messages
# Create your views here.

@login_required(login_url="member") #จะเรียกใช้ function panel ต้อง log in ก่อน 
def panel(request):
    writer = auth.get_user(request) #ดึงข้อมูล username ที่ login อยู่มาเก็บในตัวแปร writer
    blogs = Blogs.objects.filter(writer=writer) #ดึงข้อมูล blog ตามชื่อผู้เขียนมาแสดง
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views")) #การหายอด view รวม
    return render(request,"backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total})

@login_required(login_url="member")
def displayForm(request):
    writer = auth.get_user(request) #ดึงข้อมูล username ที่ login อยู่มาเก็บในตัวแปร writer
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views")) #การหายอด view รวม
    categories = Category.objects.all()
    return render(request,"backend/blogForm.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})

@login_required(login_url="member")
def insertData(request):
    try:
        if request.method == "POST" and request.FILES["image"]: #เช็คว่าส่งข้อมูลเขียน blog มาเป็น POST และส่งไฟล์ image มาด้วย
            datafile= request.FILES["image"] #เก็บไฟล์ที่ส่งมาในตัวแปร datafile
            #รับค่าจากฟอร์ม
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            writer = auth.get_user(request) #รับข้อมูลของนักเขียนจากคนที่ login
       
            #ตรวจสอบค่าว่าง
            if name == "" or category == "" or description == "" or content == "":
                messages.info(request,"กรุณาระบุข้อมูลให้ครบถ้วน")
                return redirect('displayForm')
            else :  
                #ตรวจสอบประเภทของไฟล์ที่ส่งมาว่าเป็น image รึเปล่า
                if str(datafile.content_type).startswith("image"):    
                    #อัพโหลดรูป
                    fs = FileSystemStorage()
                    img_url="blogImage/"+datafile.name
                    filename = fs.save(img_url,datafile)
                    #บันทึกข้อมูลบทความลงใน DB
                    blog = Blogs(name = name,category_id=category,description=description,content=content,writer=writer,image=img_url)
                    blog.save()
                    messages.info(request,"บันทึกข้อมูลเรียบร้อย")
                    return redirect("displayForm")
                else:
                    messages.info(request,"ไฟล์ที่ Upload ไม่รองรับ กรุณาอัพโหลดไฟล์รูปภาพอีกครั้ง")
                    return redirect("displayForm")
    except: 
        return redirect("displayForm")
@login_required(login_url="member")    
def deleteData(request,id): #การลบบทความ
    try:
        blog=Blogs.objects.get(id=id)
        fs=FileSystemStorage()
        fs.delete(str(blog.image)) #ลบรูปออกจาก server โดยส่ง path ไป
        blog.delete() #ลบข้อมูลจากฐานข้อมูล (ยังไม่ลบภาำปก จาก server เนื่องจากใน table blog เก็บ path)
        return redirect('panel')
    except :
        return redirect('panel')

@login_required(login_url="member")
def editData(request,id): #ดึงข้อมูลมาแสดง
    writer = auth.get_user(request) #ดึงข้อมูล username ที่ login อยู่มาเก็บในตัวแปร writer
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views")) #การหายอด view รวม
    categories = Category.objects.all()
    blogEdit = Blogs.objects.get(id=id)
    return render(request,"backend/editForm.html",{"blogEdit":blogEdit,"writer":writer,"blogCount":blogCount,"total":total,"categories":categories})

@login_required(login_url="member")
def updateData(request,id):
    try : 
        if request.method == "POST":
            #ดึงข้อมูลจากยทความที่ต้องการแก้ไขมาใช้งาน
            blog = Blogs.objects.get(id=id)
            #รับค่าจากฟอร์ม
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]

            if name == "" or category == "" or description == "" or content == "":
                messages.info(request,"กรุณาระบุข้อมูลให้ครบถ้วน")
                return redirect('editData',id)
            else : 
                #อัพเดทภาพปก
                if request.FILES["image"]:
                    datafile= request.FILES["image"] #เก็บไฟล์ที่ส่งมาในตัวแปร datafile
                    if str(datafile.content_type).startswith("image"):
                        #ลบ ภาพ ที่อยู่ใน media ออกไป
                        fs=FileSystemStorage()
                        fs.delete(str(blog.image))
                        #อัพเดทข้อมูล
                        blog.name = name
                        blog.category_id = category
                        blog.description = description
                        blog.content = content
                        #การเพิ่มภาพใหม่ 
                        img_url="blogImage/"+datafile.name
                        filename = fs.save(img_url,datafile)
                        blog.image = img_url
                        blog.save()
                                
                        return redirect("panel")    
                    else:
                        messages.info(request,"ไฟล์ที่ Upload ไม่รองรับ กรุณาอัพโหลดไฟล์รูปภาพอีกครั้ง")
                        return redirect('editData',id)
            
        else: 
            messages.info(request,"อัพเดทข้อมูลไม่สำเร็จ")
            return redirect('editData',id)
    except :
        return redirect("panel") 