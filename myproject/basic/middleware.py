from django.http import JsonResponse
import re,json
import jwt
from django.conf import settings


class basicMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    

    def __call__(self,request):
        print(request,"hello")
        print(request.method,'method')
        print(request.path)
        response=self.get_response(request)
        return response
    
class SscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path in ["/job1/","/job2/"]):
            ssc_result=(request.GET.get("ssc"))
            if( ssc_result !='True'):
                return JsonResponse({"error":"you should qualify ssc for applying this job"},status=400)
        return self.get_response(request)
        


class MedicalfitMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path =="/job1/"):
            medical_fit_result=(request.GET.get("medically_fit"))
            if( medical_fit_result !='True'):
                return JsonResponse({"error":"yor are not medically fit apply for this job"},status=400)
        return self.get_response(request)    

    
class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response 
    def __call__(self,request):
        if(request.path in["/job1/","/job2/"]):
            age_checker=(int(request.GET.get("age",17)))
            if(not(18<=age_checker<=25)):
        
                return JsonResponse({'error':"your age in b/w 18 and 25 "},status=400)
        return self.get_response(request)

from django.http import JsonResponse
import json
from basic.models import Users

class UserMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if(request.path=="/signUp/"):
            data=json.loads(request.body)
            username=data.get("username")
            if not username:
                return  JsonResponse({"error":"username is required"},status=400)
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username must contain the 3 to 20 characters"},status=400)
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not start with the . or _"},status=400)
            if not re.match(r"^[a-zA-Z0-9._]+$",username):
                return JsonResponse({"error":"username should contain numbers,letters,dot,underscore"},status=400)
            if ".." in username or "__" in username:
                return JsonResponse({"error":"cannot have .. or __"},status=400)
            return self.get_response(request)


class emailMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if (request.path=="/signUp/"):
            data=json.loads(request.body)
            email=data.get("email")
            if not email:
                return JsonResponse({"error":"email should not be empty"})
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                return JsonResponse({"error":"invalid email format"},status=400)
            if Users.objects.filter(email=email).exists():
                    return JsonResponse(
                    {"error": "This email is already registered. Please use another email."},
                    status=400
                )

        return self.get_response(request)


class passwordMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if (request.path=="/signUp/"):
            data=json.loads(request.body)
            password=data.get("password")
            # 1️⃣ Empty password
            if not password:
                return JsonResponse({"error": "password is required"}, status=400)

            # 2️⃣ Minimum length
            if len(password) < 6:
                return JsonResponse({"error": "password must be at least 6 characters long"}, status=400)

            # 3️⃣ At least one letter
            if not re.search(r"[A-Za-z]", password):
                return JsonResponse({"error": "password must contain at least one letter"}, status=400)

            # 4️⃣ At least one digit
            
            if not re.search(r"[0-9]", password):
                return JsonResponse({"error": "password must contain at least one number"}, status=400)

            # 5️⃣ At least one special character
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                return JsonResponse({"error": "password must contain at least one special character"}, status=400)

        return self.get_response(request)    


class token_Middleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request): 
        if request.path=="/users/":
            token=request.headers.get("Authorization")
            print(token,"token")
            if not token:
                return JsonResponse({"error":"Autherization token is missing"})
            token_value=token.split(" ")[1]
            print(token_value)
            try:
                decode_data=jwt.decode(token_value,settings.SECRET_KEY,algorithms=["HS256"])
                print(decode_data,"decode_data")
                
                request.token_data=decode_data
                
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error":"token has expired,please login"})
            except jwt.exceptons.InvalidSignatureError:
                return JsonResponse({"error":"invalid token signature"})




        return self.get_response(request)       


