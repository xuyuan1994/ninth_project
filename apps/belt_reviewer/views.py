from django.shortcuts import render,redirect
from .models import *
import bcrypt
# Create your views here.
def basic(request):
    return render(request,'basic.html')
def register(request):
    valid,response=Users.objects.validate_registration(request.POST)
    if valid:
        request.session['message']="successfully registered"
        Users.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],password= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
    else:
        request.session['message']=response
    return render(request,'result.html')
def login(request):
    
    valid,response=Users.objects.validate_login(request.POST)
    if valid:
        user=Users.objects.get(email=request.POST['email'])
        context={
            "user":user,
             "reviews":Reviews.objects.all().order_by('-id')
        }
        request.session['logged_id']=user.id
        return render(request,'main_page.html',context)
    else:
        request.session['message']=response
        return render(request,'result.html')
def add_review(request):
   
    return render(request,'add_review.html')
def reviews(request):
    try: 
        Books.objects.get(title=request.POST['title'])
    except:    
        Books.objects.create(title=request.POST['title'],author=request.POST['author'])
    
    Reviews.objects.create(rating=request.POST['rating'],comment=request.POST['review'],books=Books.objects.get(title=request.POST['title']),users=Users.objects.get(id=request.session['logged_id']))
    context={
        "title": request.POST['title'],
        "author":request.POST['author'],
        "reviews": Reviews.objects.filter(books=Books.objects.get(title=request.POST['title']))
    }
    return render(request,'comments.html',context)
def user(request,user_id):
    print Users.objects.get(id=4).name
    context={
        "user":Users.objects.get(id=user_id),
        "reviews":Reviews.objects.filter(users=Users.objects.get(id=request.session['logged_id']))
    }
    return render(request,'user.html',context)