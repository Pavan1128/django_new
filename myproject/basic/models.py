from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField(unique=True)


class Users(models.Model):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=100,unique=True)

class Movies(models.Model):
    movie_name=models.CharField(max_length=100)
    release_date=models.CharField(max_length=100)
    budget=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)







