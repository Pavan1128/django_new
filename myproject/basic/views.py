from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from basic.models import Student
from django.views.decorators.csrf import csrf_exempt 



# Create your views here.

def sample(request):

    return HttpResponse ("Welcome to django")


def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        return JsonResponse({"status":"ok","db":"connected"})
    except Exception as e:
        return JsonResponse({"status":"error","db":str(e)})

@csrf_exempt
def addstudent(request):
    print(request.method)
    if request.method=="POST":
        data=json.loads(request.body)
        student=Student.objects.create(
            name=  data.get('name'),
            age=data.get('age'),
            email= data.get('email')
            )
        
      
       
        
        return JsonResponse({"status":"success","id":student.id},status=200)
    return JsonResponse({"error":"use post method"},status=400)

# @csrf_exempt
# def post(request):
#     print(request.method)
#     if request.method=="POST":
#         data=json.loads(request.body)
#         post=Post1.objects.create(
#             name=  data.get('post_name'),
#             type=data.get('post_type'),
#             date= data.get('post_date'),
#             descrption=data.get('post_descrption')
#             )

           
#         return JsonResponse({"status":"success","id":post.id},status=200)
#     return JsonResponse({"error":"use post method"},status=400)
        
        



def get_all_records(request):
    data = Student.objects.all().values('name', 'age', 'email')
    return JsonResponse(list(data), safe=False)

def get_student_by_id(request, id):
    try:
        student = Student.objects.get(id=id)
        data = {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "email": student.email
        }
        return JsonResponse(data, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    


def get_students_age_20_plus(request):
    
    students = Student.objects.filter(age__gte=20).values('name', 'age', 'email')
    
    
    return JsonResponse({"data":list(students)}, safe=False)

