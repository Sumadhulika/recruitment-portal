from ast import Constant
from itertools import count
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib import messages
from .models import CustomUser,CandidateDetails
from django.http import JsonResponse
from django.template import loader
from datetime import datetime
from app.forms import candidateform,registration
from django_serverside_datatable.views import ServerSideDatatableView
from django.db.models import F
from django.contrib.auth import authenticate, login,logout
from datetime import date
from json import dumps
from datetime import datetime,date
from datetime import date, timedelta
import logging
from django.db.models import Count
from itertools import groupby
from operator import itemgetter
from django.contrib.auth.hashers import make_password



logger = logging.getLogger('django')

# -----------------method to perform login action----------------------------------
def my_login(request):
    try:
        logger.info("Logging to recruitmentportal")
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid email or password")
                return render(request, 'login.html')
            logger.info("loggingin with email= %s,password=%s",email,password)
            if user.check_password(password) and user.is_active:
                auth=authenticate(email=email,password=password)
                print(auth)
                request.session['username'] = user.username
                request.session['accesslable'] = user.accesslable
                admin=1
                hr=2
                if user.accesslable == admin:
                    if user.password.startswith('pbkdf2_sha256'):
                        login(request, user)

                    return redirect('/adminpage/')
                elif user.accesslable == hr:
                    if user.password.startswith('pbkdf2_sha256'):
                        login(request, user)
                    return redirect('/employee/')
                else:
                    messages.error(request, "Invalid login detail")
                    return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    except:
        logger.error("An error occurred while logging.")

#-----------------method for Adding candidates------------------------------------

def candidate_registration(request):
    username = request.session.get('username')
    accesslable = request.session.get('accesslable')
    logger.info("Adding candidates")
    try:
        if request.method == "POST":
            form = candidateform(request.POST, request.FILES)
            if form.is_valid():
                details = form.save(commit=False)
                d = form.cleaned_data
                exp = form.cleaned_data.get('experience')
                today = datetime.today()
                expdate = datetime(today.year - exp, today.month, today.day)
                details.date = expdate
                details.save()
                form.save_m2m()
                messages.success(request, 'Registration Successful')
                logger.info("adding candidate %s", d)
                form = candidateform()
                return render(request, 'candidate_reg.html', {"form": form, 'username': username, 'accesslable': accesslable})
            else:
                messages.error(request, 'Form validation failed, please check your inputs and try again.')
                logger.error("An error occurred while adding the candidate. Form validation failed.")
                return render(request, 'candidate_reg.html', {"form": form, 'username': username, 'accesslable': accesslable})

        else:
            form = candidateform()
        return render(request, 'candidate_reg.html', {"form": form, 'username': username, 'accesslable': accesslable})
    except Exception as e:
        logger.error("An error occurred while adding the candidate: %s", str(e))
        messages.error(request, 'Registration Unsuccessful')
        return render(request, 'candidate_reg.html', {"form": form, 'username': username, 'accesslable': accesslable})




#-----------------method for Adding Employees-------------------------------------
def employee_registration(request):
    username = request.session.get('username')
    accesslable = request.session.get('accesslable')
    logger.info("Adding employees")
    try:
        if request.method == "POST":
            form = registration(request.POST)
            if form.is_valid():
                d=form.cleaned_data
                email = form.cleaned_data.get('email')
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request,'This email already exists')
                    logger.error("This email already exists")
                    return render(request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})
                else:
                    details = form.save(commit=False)
                    password = form.cleaned_data.get('password')
                    details.password = make_password(password)
                    details.is_active = True
                    details.save()
                    messages.success(request,'Registration Successful')
                    logger.info("adding employee  %s",d)
                    form = registration()
                    return render (request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})
            else:
                messages.error(request,'Registration Unsuccessful')
                logger.error("An error occurred while adding the employee.")
                return render(request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})
        else:
            form = registration()
        logger.info("adding employee  username = %s and accesslable = %s", username,accesslable)
        return render(request,'employee_reg.html',{"form":form,'username':username,'accesslable':accesslable})
    except:
        logger.error("An error occurred while adding the employee.")
        messages.error(request, 'An error occurred while adding the employee')
        return render(request, 'employee_reg.html', {"form":form,'username':username,'accesslable':accesslable})



#-----------------method for returning candidate details page----------------------------------
def viewcandidate(request):
    logger.info("viewing candidatedetails")
    try:
        username = request.session.get('username')
        accesslable = request.session.get('accesslable')
        context={'username':username
            ,'accesslable':accesslable}
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
def my_logout(request):
    try:
      del request.session['username']
      del request.session['accesslable']
      logger.info("loggedout")
    except:
        logger.error("An error occurred while loggingout.")

    messages.error(request,"Loggedout successfully")
    return redirect ('/home/')