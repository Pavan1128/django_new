"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from basic.views import sample
from basic.views import health,addstudent,get_all_records,get_student_by_id,get_students_age_20_plus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sample/',sample),

    path('health/',health),
    path('student/',addstudent),
    path('get_all/',get_all_records),
    path('get_id/<int:id>/',get_student_by_id),
    path("get>20/",get_students_age_20_plus)
]
