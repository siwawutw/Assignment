from django.shortcuts import render
from blogs.models import Blogs
from django.db.models import Sum
# Create your views here.
def panel(request):
    writer = "admin"
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum("views")) #การหายอด view รวม
    return render(request,"backend/index.html",{"blogs":blogs,"writer":writer,"blogCount":blogCount,"total":total})