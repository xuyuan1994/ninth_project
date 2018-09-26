from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self,form_data):
        errors=[]
        if len(form_data['name'])<2:
            errors.append('first name is too short')
        if len(form_data['alias'])<2:
            errors.append('last name is too short')
        if len(form_data['password'])<8:
            errors.append('password is too short')
        if not EMAIL_REGEX.match(form_data['email']):

            errors.append('email is not valid')
        if form_data['password']!=form_data['confirm']:
            errors.append('password and confirm password must match')
        try:
            user=self.get(email=form_data['email'])
            errors.append("this email has already been registered")
            return (False, errors)
        except:
            if len(errors)>0:
                return (False,errors)
            else:
                return (True,errors)
    def validate_login(self,form_data):
        errors=[]
        try:
            user=self.get(email=form_data['email'])
            if bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
                print ('correct2')
                return (True,errors)
            else:
                errors.append("either your username or password is invalid")
                return (False,errors)
        except:
            errors.append('Incorrect username or password')
            return (False, errors)
class Users(models.Model):
    name=models.CharField(max_length=30)
    alias=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    objects = UserManager()
class Books(models.Model):
    title=models.CharField(max_length=30)
    author=models.CharField(max_length=30)

class Reviews(models.Model):
    rating=models.IntegerField()
    comment=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    users = models.ForeignKey(Users, related_name="reviews")
    books = models.ForeignKey(Books, related_name="reviews")