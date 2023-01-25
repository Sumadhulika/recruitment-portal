from ast import Constant
from itertools import count
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib import messages
from app.models import *
from django.http import JsonResponse
from django.template import loader
from datetime import datetime
from app.forms import candidateform,registration
from django_serverside_datatable.views import ServerSideDatatableView
from django.db.models import F
from datetime import date
from json import dumps
from datetime import datetime,date
from datetime import date, timedelta
import logging
from django.db.models import Count
from itertools import groupby
from operator import itemgetter


logger = logging.getLogger('django')

# -----------------method to perform login action----------------------------------
def login(request):
    global m,cursor,d
    try:
        if request.method=="POST":
            m=sql.connect(host="localhost",user="root",password="Suma@2000",database="recruitment")
            cursor=m.cursor()
            email=request.POST['email']
            password=request.POST['password']
            c= f"select * from app_appuser where email='{email}' and password='{password}'"
            cursor.execute(c)
            t=tuple(cursor.fetchall())
            logger.info("loggingin with email= %s,password=%s",email,password)
            if(t):
                username=t[0][2]
                accesslable=t[0][6]
                request.session['username']=username
                request.session['accesslable']=accesslable
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
        else:
            return render(request,'login.html')
    except:
        logger.error("An error occurred while logging.")

#-----------------method for Adding candidates------------------------------------
def candidate_registration(request):
    username = request.session.get('username')
    accesslable = request.session.get('accesslable')
    try:
        if request.method=="POST":
                form=candidateform(request.POST)
                if form.is_valid():
                    details=form.save(commit=False)
                    d=form.cleaned_data
                    exp=form.cleaned_data['experience']
                    today=datetime.today()
                    expdate=datetime(today.year-exp,today.month,today.day)
                    details.date=expdate
                    details.save()
                    form.save_m2m()
                    messages.success(request,'Registration Successful')
                    logger.info("adding candidate  %s",d)
                    return render (request,'candidate_reg.html',{"form":form,'username':username,'accesslable':accesslable})
                else:
                    messages.error(request,'Registration Unsuccessful')
                    return render (request,'candidate_reg.html',{"form":form,'username':username,'accesslable':accesslable})
        else:
            form=candidateform(request.POST)
        return render (request,'candidate_reg.html',{"form":form,'username':username,'accesslable':accesslable}) 
    except:
        logger.error("An error occurred while adding the candidate.")


#-----------------method for Adding Employees-------------------------------------
def employee_registration(request):
    username = request.session.get('username')
    accesslable = request.session.get('accesslable')
    try:
        if request.method=="POST":
                form=registration(request.POST)
                if form.is_valid():
                    d=form.cleaned_data
                    form.save()
                    messages.success(request,'Registration Successful')
                    logger.info("adding employee  %s",d)
                    return render (request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})
                else:
                    messages.error(request,'Registration Unsuccessful')
                    return render (request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})
        else:
            form=registration(request.POST)
        logger.info("adding employee  username = %s and accesslable = %s", username,accesslable)
        return render (request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})    
    except:

        logger.error("An error occurred while adding the employee.")



#-----------------method for returning candidate details page----------------------------------
def viewcandidate(request):
    try:
        username = request.session.get('username')
        accesslable = request.session.get('accesslable')
        context={'username':username
            ,'accesslable':accesslable}
        logger.info("viewing candidatedetails")
        return render(request,'viewcandidate.html',context)
    except:
        logger.error("An error occurred while veiwing candidatedetails")


#-----------------method for serializing the data to jsonformate----------------------------------
def json_date_handler(obj):
  if isinstance(obj, (datetime, date)):
    return obj.isoformat()
  else:
    raise TypeError("Type %s not serializable" % type(obj))


#-----------------method for sending data in json formate to datatables----------------------------------
def dataJson(request):
    username = request.session.get('username')
    accesslable = request.session.get('accesslable')
    try:
        candidateDetails = CandidateDetails.objects.all().values()
        cd=CandidateDetails.objects.all()
        today = date.today()
        skilllist = []
        for candidate in cd:
            difference_in_years = today.year - candidate.date.year
            candidate.experience = difference_in_years
            candidate.save()
            s = CandidateDetails.objects.get(id=candidate.id).skills.all()
            li = []
            for i in s:
                li.append(i.skills)
            skilllist.append(li)
        # candidateDetails = CandidateDetails.objects.annotate(skills='skills')
        candidateDetails = candidateDetails.values('first_name','last_name','email','qualifications_id' ,'experience','contact','address')
        data = {
        'data': list(candidateDetails),
        'skills':skilllist,
        'draw': request.GET.get('draw'),
        'recordsTotal': CandidateDetails.objects.all().count(),
        'recordsFiltered': CandidateDetails.objects.all().count()
        }
        json_data = json.dumps(data, default=json_date_handler)
        return JsonResponse(data,safe=False, content_type='application/json')
    except Exception as e:
        logger.error("An error occurred while processing the data.")
        


#-----------------method for returning homepage----------------------------------
def home(request):
    try:
        logger.info("homepage loaded")
        return render(request,'home.html')
    except:
        logger.error("An error occurred while loading homepage.")



#-----------------method for returning admin accesspage---------------------------
def adminpage(request):
    try:
        username = request.session.get('username')
        accesslable = request.session.get('accesslable')
        context={'username':username
        ,'accesslable':accesslable}
        logger.info("logined with username = %s and accesslable = %s", username,accesslable)
        return render(request,'admin.html',context)
    except:
        logger.error("An error occurred while loggingout.")



#-----------------method for returning employee accesspage------------------------
def employee(request):
    try:
        username = request.session.get('username')
        accesslable = request.session.get('accesslable')
        context={'username':username,
            'accesslable':accesslable}
        logger.info("logined with username = %s and accesslable = %s", username,accesslable)
        return render(request,'employee.html',context)
        
    except:
        logger.error("An error occurred while loggingout.")
       


# -----------------method to perform logout action-------------------------------
def logout(request):
    try:
      del request.session['username']
      del request.session['accesslable']
      logger.info("loggedout")
    except:
        logger.error("An error occurred while loggingout.")

    messages.error(request,"Loggedout successfully")
    return redirect ('/home/')