from datetime import datetime
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
import re
import bcrypt

class UserManger(models.Manager):
    def validator_registeration(self, postData):
        errors  = {}

        try:
            user = self.get(email=postData['email'])
            errors['exsited_email'] = f"{postData['email']} is already registered"
        except:
            pass
        
        if len(postData['name']) < 2 :
            errors['name'] = 'Name must be at least of two characters'

        if len(postData['alias']) < 2 :
            errors['alias'] = 'Alias must be at least of two characters'
        
        if len(postData['password']) < 8:
            errors['password'] = 'password must be at least of eight characters'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['invalid_email'] = 'invalid email address'
        
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'password and confirm password are not the same'
        
        birth_date = postData['birth_date'].split('-') 
        year = int(birth_date[0])
        month = int(birth_date[1])
        day = int(birth_date[2])

        now = datetime.now()
        now_year = int(now.strftime("%Y"))
        now_month = int(now.strftime("%m"))
        now_day = int(now.strftime("%d"))

        if now_year - year < 16 :
            errors['age'] = 'The user must be 16 or older to register'
        elif now_year - year == 16 :
            if  not now_month == month and  not now_day == day:
                errors['age'] = 'The user must be 16 or older to register'



        # if postData['birth_date']

        return errors
    
    def validator_login(self, postData):
        errors = {}
        try:
            user = self.get(email=postData['email'])

            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                pass
            else:
                errors['failed_password'] = "email and password are not matched"

        except:
            errors['existed_email'] = f"{postData['email']} is not registered"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255, default="") 
    alias = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255, default="")
    birth_date = models.DateField()
    friends = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManger()

def create_user(postData):
    name = postData['name']
    alias = postData['alias']
    email = postData['email']
    birth_date = postData['birth_date']
    password  = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode() 
    User.objects.create(name=name, email=email, password=password, birth_date=birth_date, alias=alias)
    return User.objects.last()

def get_user_details(email):
    user = User.objects.get(email=email)
    user_details = {
        'id': user.id,
        'name': user.name,
        'alias': user.alias,
        'email': user.email,
        # 'created_at': user.created_at,
        # 'updated_at': user.updated_at,
    }

    return user_details

