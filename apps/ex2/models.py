from __future__ import unicode_literals
from django.db import models
import re, datetime
import bcrypt

NAME_REGEX = re.compile(r'^[a-zA-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def reg_validation(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name_length'] = "First name must be greater than 2 characters!"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name_format'] = "Invalid first name format!"
        if len(postData['last_name']) < 2:
            errors['last_name_length'] = "Last name must be greater than 2 characters!"
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name_format'] = "Invalid last name format!"
        if len(postData['email']) < 1:
            errors['email_empty'] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Invalid email format!"
        else:
            users = User.objects.all()
            for user in users:
                if user.email == postData['email']:
                    errors['taken_email'] = "This email has already been taken!"
                    break
        if len(postData['bday']) < 1:
            errors['bday_length'] = "Birthday cannot be empty!"
        elif datetime.datetime.strptime(postData['bday'], "%Y-%m-%d") > datetime.datetime.today():
            errors['future_birth'] = "Birthday must be a day in the past!"
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be at least 8 characters long!"
        elif postData['password'] != postData['repeat_password']:
            errors['no_match'] = "Password and repeat password do no match!"         
        return errors

    def login_validation(self, postData):
        errors = {}
        email_exists = False
        users = User.objects.all()
        for user in users:
            if user.email == postData['login_email']:
                email_exists = True
                if not bcrypt.checkpw(postData['login_password'].encode(), user.pass_hs.encode()):
                    errors['incorrect_pw'] = "Incorrect password!"
                break
        if not email_exists:
            errors['no_email'] = "This email address doesn't exist!"
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    bday = models.DateField()
    pass_hs = models.CharField(max_length = 255)
    objects = UserManager()
