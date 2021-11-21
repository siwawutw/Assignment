from django.shortcuts import redirect, render,redirect

# Create your views here.
def index(request):
    return render(request,"backend/login_register.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if username == "" or email == "" or password == "" or repassword == "":
            print("กรุณากรอกข้อมูลให้ครบถ้วน")
            return redirect('member')
        
    return redirect('member')