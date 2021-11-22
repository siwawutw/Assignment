from django.http import request
from django.shortcuts import redirect, render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.
def index(request):
    return render(request,"backend/login_register.html")

def register(request): #สร้างบัญชีผู้ใช้
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if username == "" or email == "" or password == "" or repassword == "":
            messages.info(request,"กรุณาระบุข้อมูลให้ครบถ้วน")
            return redirect('member')
        else: #ข้อมูลครบ สร้างบัญชีผู้ใช้
            if password == repassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username นี้มีคนใช้แล้ว")
                    return redirect('member')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email นี้มีคนใช้แล้ว")
                    return redirect('member')
                else:
                    user=User.objects.create_user(
                    username = username, #ชื่อฟิลด์ = ชื่อตัวแปร
                    email = email,
                    password = password
                )
                    user.save()
                    messages.info(request,"สร้างบัญชีสำเร็จ")
                    return redirect('member')            
            else:
                messages.info(request,"กรุณาระบุรหัสผ่านให้ตรงกัน")
                return redirect('member')

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user=auth.authenticate(username=username,password=password)
    
    if user is not None:
        auth.login(request,user)
        return redirect('panel') #login สำเร็จ redirect ไปที่หน้า writer panel
    else:
        messages.info(request,"ไม่พบข้อมูลบัญชีผู้ใช้ หรือ รหัสผ่านไม่ถูกต้อง")
        return redirect('member')

def logout(request):
    auth.logout(request)
    return redirect('member')