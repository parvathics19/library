from distutils.command.upload import upload
from msilib.schema import Class
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

# Create your models here.
class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    mobile=models.IntegerField(null=True)
class Category(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='category')

class book(models.Model):
    image=models.ImageField(upload_to='book')
    description=models.TextField()
    name=models.TextField()
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)


def get_expiry():
    return datetime.today() + timedelta(days=15)
class issue(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    book_id=models.ForeignKey(book,on_delete=models.CASCADE,null=True,blank=True)
    request=models.IntegerField(null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(default=get_expiry,null=True)
    fine=models.IntegerField(null=True)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)

