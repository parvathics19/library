import random
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from .models import*
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from datetime import date
from django.db import connection
cursor = connection.cursor()
# Create your views here.
def home(request):
    return render (request,'home.html')

def signin(request):
    if request.method=='POST':
       uname=request.POST['uname']
       pssw=request.POST['pswd']
       user=auth.authenticate(username=uname,password=pssw)
        
        
       if user is not None:
            auth.login(request,user)
                
            return redirect('home')
    return render (request,'signin.html')

def sendMail(email,password,username):       
    subject = 'LMS '
    message = 'Welcome, Explore the world of reading, your Username='+username+' and Password='+password+' thankyou, '
    html_content = '<p>Welcome</p><br><p> You have registered successfully...</p><p> your <strong>username='+username+'</strong> and <strong>password='+password +'</strong></p><br><p> Thankyou</p>'
    
    recipient = email    #  recipient =request.POST["inputTagName"]
    send_mail(subject, 
        message, settings.EMAIL_HOST_USER, [recipient],html_message=html_content)


def generateOTP(request) :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    password = ""
 
   # length of password can be changed
   # by changing value in range
    for len in range(8):
        random_char = random.choice(digits)
        password += random_char
    
    return JsonResponse({'status':password})
def signup(request):
    
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['uname']
        email=request.POST['email']
        mobile=request.POST['mobile']
        pssw=request.POST.get('pssw')
        cpssw=request.POST.get('cpssw')
        if pssw==cpssw:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists!!!!!!')
                return redirect('signup') 

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists!!!!!!')
                return redirect('signup') 

            else:
                user =User.objects.create_user(  #create_user 
                    first_name=fname,
                    last_name=lname,
                    username=username,
                    email=email,
                    password=pssw )
                user.save()
                user = User.objects.get(id=user.id)
                userpro=UserProfile(user=user,mobile=mobile)
                userpro.save()
                sendMail(email,pssw,username)
                return redirect('signin')
    return render (request,'signup.html')

def logout(request):   
    auth.logout(request)
    return redirect('home')

def add_category(request):
    category=Category.objects.all()
    if request.method=='POST':
        name=request.POST['category']

        cate=Category(
            name=name,
            
        )
        cate.save()
        return redirect('show_category')  
    return render(request,'admin/addcategory.html',{'category':category})

def show_category(request):  #to show
    category=Category.objects.all()
    return render(request,'admin/showcategory.html',{'category':category})

def delete_category(request,pk):
    category=Category.objects.get(id=pk)
    category.delete()
    return redirect('show_category')

def add_book(request):
    category=Category.objects.all()


    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES.get('image')
        description=request.POST['description']
        category=request.POST['category']
        cat = Category.objects.get(id=category)
        addbook=book( name=name,image=image,description=description,category_id=cat)
        addbook.save()

    return render(request,'admin/addbook.html',{'category':category})

def show_book(request):
    books=book.objects.all()

    return render(request,'admin/showbook.html',{'books':books}) #2nd value,, 1st key

def delete_book(request,pk):
    bk=book.objects.get(id=pk)
    bk.delete()
    return redirect('show_book')



def view_users(request):
    users=UserProfile.objects.all()
    return render(request,'admin/viewusers.html',{'users':users})
def delete_user(request,pk):
    user=User.objects.get(id=pk) 
    user.delete()                                        
    return redirect('view_users')


def view_category(request):
    view=Category.objects.all()
    return render(request,'user/viewcategory.html',{'view':view})


def view_book(request,pk):
    vw=book.objects.filter(category_id=pk)
    return render(request,'user/viewbooks.html',{'vw':vw})

def req_booking(request,pk):
    req_book= book.objects.get(id=pk)
    cat = Category.objects.get(id=req_book.category_id.id)
    user = request.user.id
    usr = User.objects.get(id=user)
    issu = issue(
        user_id=usr,
        book_id=req_book,
        request =1,
        category_id=cat,
    )
    issu.save()
    return redirect('view_booking')

def view_booking(request):
    user=request.user.id
    bkng=issue.objects.filter(user_id=user)
    delay_date = bkng.end_date-bkng.start_date
    print(delay_date)
    return render(request,'user/viewbooking.html',{'bkng':bkng})


def edit_profile(request):
    user_id = request.user.id
    edit_user = User.objects.get(id = user_id)
    if request.method=='POST':
        edit_user.first_name = request.POST['fname']
        edit_user.last_name = request.POST['lname']
        edit_user.username = request.POST['username']
        edit_user.email = request.POST['email']
        edit_user.save()
        return redirect ('home')
    return render(request,'user/profile_edit.html')


def admin_booking(request):

    # bookings=issue.objects.all()
    cursor.execute( 'select li.id as id,lb.name as book_name,li.end_date as end_date,li.start_date as start_date,lb.image as image,CURDATE() as today,case when CURRENT_DATE()-li.end_date>0 then CURRENT_DATE()-li.end_date  else 0 end as delay_date,case when CURRENT_DATE()-li.end_date>0 then CURRENT_DATE()-li.end_date*5  else 0 end as fine from libraryapp_issue li join libraryapp_book lb on  li.book_id_id = lb.id join libraryapp_userprofile lu on li.user_id_id = lu.user_id')
    bookings = cursor.fetchone()
   
    li=[]
    for i in bookings:
        li.append(i)
    print(li)
    for i in li:
        print(i)
    # li=[]
    # for ib in bookings:
    #     issdate=str(ib.start_date.day)+'-'+str(ib.start_date.month)+'-'+str(ib.start_date.year)
    #     expdate=str(ib.end_date.day)+'-'+str(ib.end_date.month)+'-'+str(ib.end_date.year)
    #     #fine calculation
    #     days=(date.today()-ib.start_date)
    #     print(date.today())
    #     d=days.days
    #     fine=0
    #     if d>15:
    #         day=d-15
    #         fine=day*10


    #     books=list(book.objects.filter(isbn=ib.))
    #     students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
    #     i=0
    #     for l in books:
    #         t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
    #         i=i+1
    #         li.append(t)


    return render(request,'admin/booking.html',{'bookings':li})

def reject_booking(request,pk):
    booking=issue.objects.get(id=pk)
    booking.delete()
    return redirect('admin_booking')

def approve(request,pk):
    aprve=issue.objects.get(id=pk)
    aprve.request=2
    aprve.start_date = datetime.now()
    aprve.save()
    return redirect('admin_booking')
