from ast import Constant
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib import messages
from app.models import *
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from app.forms import candidateform,registration
from django_serverside_datatable.views import ServerSideDatatableView
from django.db.models import F
from datetime import date



# -----------------method to perform login action----------------------------------
def login(request):
    global m,cursor,d
    if request.method=="POST":
        
        m=sql.connect(host="localhost",user="root",password="Suma@2000",database="recruitment")
        cursor=m.cursor()
        email=request.POST['email']
        password=request.POST['password']
        # vams = appuser.objects.get(email=email)
        # print(vams.username,"*******")
        # login(request, vams, backend='django.contrib.auth.backends.ModelBackend')
        c= f"select * from app_appuser where email='{email}' and password='{password}'"
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        print(t)
        if(t):
            print(t)
            username=t[0][2]
            accesslable=t[0][6]
            request.session['username']=username
            request.session['accesslable']=accesslable
            d={'username':username}
            admin="1"
            employee="2"
            if accesslable==admin:
                return redirect ('/adminpage/')
            if accesslable==employee:
                return redirect ('/employee/')
            else:
                messages.error(request,"invalid login detail")
                return render (request,'login.html')
        else:
            messages.error(request,"invali login detail")
            return render (request,'login.html')
    return render(request,'login.html')



#-----------------method for Adding candidates------------------------------------
def candidate_registration(request):
    username = request.session.get('username')
    if request.method=="POST":
        form=candidateform(request.POST)
        print(form)
        if form.is_valid():
            
            details=form.save(commit=False)
            exp=form.cleaned_data['experience']
            today=datetime.today()
            expdate=datetime(today.year-exp,today.month,today.day)
            details.date=expdate
            details.save()
            messages.success(request,'Registration Successful')
            return render (request,'candidate_reg.html',{"form":form,'username':username})
    else:
        form=candidateform(request.POST)
    return render (request,'candidate_reg.html',{"form":form,'username':username}) 



#-----------------method for Adding Employees-------------------------------------
def employee_registration(request):
    username = request.session.get('username')
    
    if request.method=="POST":
        form=registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Successful')
            return render (request,'employee_reg.html',{"form":form,'username':username})
    else:
        form=registration(request.POST)
        
    return render (request,'employee_reg.html',{"form":form,'username':username})    



#-----------------method for viewing candidates----------------------------------
def viewcandidate(request):
    username = request.session.get('username')
    
    queryset = CandidateDetails.objects.all()
    columns = ['first_name', 'last_name', 'email','skills','experience','contact','address']
    
    return render(request,'viewcandidate.html',{'username':username})



#-----------------method for returning homepage----------------------------------
def home(request):
    return render(request,'home.html')



#-----------------method for returning admin accesspage---------------------------
def adminpage(request):
    username = request.session.get('username')
    context={'username':username}
    return render(request,'admin.html',context)




#-----------------method for returning employee accesspage------------------------
def employee(request):
    username = request.session.get('username')
    context={'username':username}
    return render(request,'employee.html',context)




# -----------------method to perform logout action-------------------------------
def logout(request):
    try:
      del request.session['username']
    except:
      pass
    messages.error(request,"Loggedout successfully")
    return redirect ('/home/')
