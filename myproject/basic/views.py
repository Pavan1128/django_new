from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from basic.models import Student
from django.views.decorators.csrf import csrf_exempt 
from basic.models import Users
from basic.models import Movies
from datetime import datetime
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
import jwt
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo




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
    elif request.method=="GET":
        result=list(Student.objects.values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    



    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")#getting id
        new_email=data.get("email")#getting email
        exsisting_student= Student.objects.get(id=ref_id)#fetch the object as per id
        # print(exsisting_student)
        exsisting_student.email=new_email #updating the email
        exsisting_student.save()
        updated_data=Student.objects.filter(id=ref_id).values().first()
        print(updated_data)
        return JsonResponse({"status":"ok","data":updated_data},status=200)
    



    elif request.method=="DELETE":
         data=json.loads(request.body)
         ref_id=data.get("id")
         delete_data=Student.objects.filter(id=ref_id).values().first()
         to_delete=Student.objects.get(id=ref_id)
         to_delete.delete()
         return JsonResponse({"status":"sucess","message":"student record successfully","data":delete_data},status=200)
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



def job1(request):
    return JsonResponse({"message":"you have successfully applied for job"},status=200)
def job2(request):
    return JsonResponse({"message":"you have successfully applied for job"},status=200)

@csrf_exempt
def signUp(request):
    if request.method=="POST":
        data=json.loads(request.body)
        print(data)
        user=Users.objects.create(
             username=  data.get('username'),
             email=data.get('email'),
             password= make_password(data.get('password')),
             
             )
    return JsonResponse({"status":"success"}) 


@csrf_exempt
def login(request):
    if request.method=="POST":
        data=json.loads(request.body)
        username=data.get('username')
        password=data.get('password')
        

        user=Users.objects.get(username=username)
        issued_time=datetime.now(ZoneInfo("Asia/Kolkata"))
        expire_time=issued_time+timedelta(minutes=1)
        it_expire_in=int((expire_time-issued_time).total_seconds()/60)
    
        if check_password(password,user.password):
            payloads={"username":username,"email":user.email,"exp":expire_time}
            
            token=jwt.encode(payloads,settings.SECRET_KEY,algorithm="HS256")

            return JsonResponse ({'status':"successfully","token":token,"time":issued_time,"expired_in":expire_time,"it expired in":it_expire_in})
        else:
            return JsonResponse({'status':'failure'})
        
@csrf_exempt
def changepassword(request):
    if request.method=="PUT":
        data=json.loads(request.body)
        ref_psd=data.get('id')
        update_psd=data.get('password')
        user=Users.objects.get(id=ref_psd)
        user.password=make_password(update_psd)
        user.save()
        update_data=Users.objects.filter(id=ref_psd).values().first()
        print(update_data)
        return JsonResponse({'satus':"password updates successfully","result":update_data})


# @csrf_exempt
# def reviews(request):
#     if (request.method == 'POST'):
#         data = json.loads(request.body)
#         rating_number=int(data.get('rating',0))
#         rating_star="*"*rating_number
#         movie=Movies.objects.create (
#         movie_name = data.get('movie_name'),
#         release_date = data.get('release_date'),
#         budget = data.get('budget'),
#         rating = rating_star
#         )
#         return JsonResponse({
#             "status": "success",
#             "movie_name": movie.movie_name,
#             "release_date": movie.release_date,
#             "budget":movie. budget,
#             "rating": movie.rating
#         })

#     return JsonResponse({"error": "Use POST method"}, status=405)



@csrf_exempt
def reviews(request):
    if request.method == 'POST':
        data = json.loads(request.body)

      

        # Convert number to stars
        rating_star = "*" * int(data.get("rating", 0))

        # Save movie
        movie = Movies.objects.create(
            movie_name=data.get("movie_name"),
            release_date=data.get("release_date"),
            budget=data.get("budget"),
            rating=rating_star
        )

        return JsonResponse({
            "status": "success","movie_name": movie.movie_name,"release_date": movie.release_date,"budget": movie.budget,"rating": movie.rating
        })

    return JsonResponse({"error": "Use POST"}, status=405)


@csrf_exempt
def receive (request):
    if request.method=="GET":
        result=list(Movies.objects.values())
        return JsonResponse({"status":"ok","data":result})
    
@csrf_exempt 
def update(request):
    if request.method=="PUT":
        data=json.loads(request.body)
        movie=Movies.objects.get(id=data.get('id'))
        if data.get("movie_name"):
            movie.movie_name=data.get('movie_name')
        if data.get("release_date"):
            movie.release_date=data.get("release_date")
        if data.get("budget"):
            movie.budget=data.get("budget")
        movie.save()    
        return JsonResponse({
    "status": "success",
    "data": {
        "id": movie.id,
        "movie_name": movie.movie_name,
        "release_date": movie.release_date,
        "budget": movie.budget,
        "rating": movie.rating
    }
})
    
# @csrf_exempt
# def delete(request):
#     data=json.loads(request.body) 
#     movie=Movies.objects.get(id=data.get('id')) 

# @csrf_exempt
# def delete(request):
#     data = json.loads(request.body)
#     movie_id = data.get('id')

#     Movies.objects.filter(id=movie_id).delete()

#     return JsonResponse({"status": "deleted"})
@csrf_exempt
def delete(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        movie_id = data.get("movie_id")

        if not movie_id:
            return JsonResponse({"status": "error", "message": "movie_id missing"})

        deleted, _ = Movies.objects.filter(id=movie_id).delete()

        if deleted == 0:
            return JsonResponse({"status": "error", "message": "Movie not found"})
        
        return JsonResponse({"status": "success", "message": "Movie deleted"})
    
    return JsonResponse({"status": "error", "message": "Use DELETE method"})


    
@csrf_exempt
def get_movies_by_budget(request):
    movies = Movies.objects.all()


    result = []
    for m in movies:
        num = int(m.budget.replace("cr", "").strip())
        if 400 <= num <= 500:
            result.append({
                "id": m.id,
                "movie_name": m.movie_name,
                "budget": m.budget,
                "release_date": m.release_date,
                "rating": m.rating,
            })

    return JsonResponse({
        "status": "success",
        "data": result
    })
@csrf_exempt
def get_rating_five(request):
    movies = Movies.objects.filter(rating="*****")

    result = []
    for m in movies:
        result.append({
            "id": m.id,
            "movie_name": m.movie_name,
            "release_date": m.release_date,
            "budget": m.budget,
            "rating": m.rating
        })

    return JsonResponse({"status": "ok", "data": result})



def update(request):
    if request.method=="PUT":
        data=json.loads(request.body)
        movies=Movies.objects.get(id=data.get('id'))
        if data.get("movie_name"):
            movies.movie_name=data.get('movie_name')
        if data.get("budget"):
            movies.movie_name=data.get('budget') 
        if data.get("release_date"):
            movies.release_date=data.get("release_date")
        if data.get("rating"):
                movies.release_date=data.get ("rating")


@csrf_exempt
def hash(request):
    if request.method=='POST':
        data=json.loads(request.body)
        print(data)
        x="pbkdf2_sha256$1000000$xgYjiScszDW2ucH6Fj6HpB$mQ615KB/BVgPL4Ot3uhpXNxn9CFLIqAZs0raAlYmBpc="
        hashed=make_password(data.get('password'))
        print(hashed)

        y=check_password(data.get('password'),x)
        return JsonResponse({"status":"success","result":y})
    
@csrf_exempt
def getdata(request):
    if request.method=="GET":
        users=list(Users.objects.values())
        print(request.token_data)
        print(request.token_data.get("username"))
        for user in users:
            if user["username"]==request.token_data.get("username"):
                 return JsonResponse({"status":"success","loggin_user":request.token_data,"data":users})
        return JsonResponse({"error":"unauthorized access"})

         
    

    
    


                

    


















  
