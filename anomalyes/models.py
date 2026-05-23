from django.db import models

class regtable(models.Model):
    name=models.CharField(max_length=150) 
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150) 
    phone=models.CharField(max_length=150) 

class uploadtable(models.Model):
    images=models.CharField(max_length=150) 
    result=models.CharField(max_length=150) 
    user_id=models.CharField(max_length=150) 

class complainttable(models.Model):
    user_id  = models.CharField(max_length=150)
    subject  = models.CharField(max_length=250)
    message  = models.TextField()
    date     = models.DateTimeField(auto_now_add=True)
    status   = models.CharField(max_length=50, default='Pending')
