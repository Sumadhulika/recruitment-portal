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
from app.views import my_login
from app.views import candidate_registration
from app.views import home
from django .conf import settings
from django.conf.urls.static import static
from app.views import adminpage
from app.views import employee
from app.views import my_logout
from app.views import employee_registration
from app.views import viewcandidate
from app.views import dataJson
urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_login/',my_login,name='my_login'),
    path('candidate_registration/',candidate_registration),
    path('home/',home),
    path('adminpage/',adminpage),
    path('employee/',employee),
    path('my_logout/',my_logout,name='my_logout'),
    path('employee_registration/',employee_registration),
    path('viewcandidate/',viewcandidate),
    path('dataJson/',dataJson,name='dataJson'),








]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)