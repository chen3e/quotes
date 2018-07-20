from django.db import models
import re
import bcrypt
from django.contrib import messages

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name_length"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name_length"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors["password_mismatch"] = "Passwords do not match"
        if not NAME_REGEX.match(postData['first_name']):
            errors["first_name_valid"] = "Invalid first name"
        if not NAME_REGEX.match(postData['last_name']):
            errors["last_name_valid"] = "Invalid last name"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address"
        emails = self.filter(email = postData['email'])
        if len(emails) > 0:
            errors["email"] = "Email already taken"
        return errors
    def validate_login(request, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(user) > 0:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                print("password match")
            else:
                errors["incorrect_password"] = "Incorrect password"  
        else:
            errors["not_registered"] = "Email not registered"
        return errors
    def validate_edit(self, request, postData):
        errors = {}
        curr_user = User.objects.get(id = request.session['current_user'])
        if len(postData['first_name']):
            if len(postData['first_name']) < 2:
                errors["first_name_length"] = "First name should be at least 2 characters"
            if not NAME_REGEX.match(postData['first_name']):
                errors["first_name_valid"] = "Invalid first name"
        if len(postData['last_name']):
            if len(postData['last_name']) < 2:
                errors["last_name_length"] = "Last name should be at least 2 characters"
            if not NAME_REGEX.match(postData['last_name']):
                errors["last_name_valid"] = "Invalid last name"
        if len(postData['email']):
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "Invalid email address"
            emails = self.filter(email = postData['email'])
            if len(emails) > 0:
                if postData['email'] == curr_user.email:
                    return errors
                errors["email"] = "Email already taken"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    objects = UserManager()