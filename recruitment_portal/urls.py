"""recruitment_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import login
from app.views import candidate_registration
from app.views import home
from app.views import adminpage
from app.views import employee
from app.views import logout
from app.views import employee_registration
from app.views import viewcandidate
from app.views import dataJson
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login),
    path('candidate_registration/',candidate_registration),
    path('home/',home),
    path('adminpage/',adminpage),
    path('employee/',employee),
    path('logout/',logout),
    path('employee_registration/',employee_registration),
    path('viewcandidate/',viewcandidate),
    path('dataJson/',dataJson,name='dataJson'),
]