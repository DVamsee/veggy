from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model
from profiles.models import User_details
from datetime import datetime


# Create your models here.
User = get_user_model()

class Products(models.Model):
    product_id = models.AutoField(
        primary_key= True,

    )
    product_name = models.CharField(max_length= 40)
    product_image = models.ImageField(upload_to='products/',default='products/dummy.jpg')
    total_quantity = models.IntegerField(default =0)
    seller = models.ForeignKey(User_details,on_delete=models.CASCADE)
    price = models.IntegerField(default = 0)
    date = models.DateTimeField(default=datetime.now())
    
    
    def __str__(self):
        return str(self.product_id)
    

    
    
class Orders(models.Model):
    order_id = models.AutoField(
        primary_key= True,

    )
    product_id = models.ForeignKey( Products,on_delete=models.CASCADE)
    seller =  models.ForeignKey(User_details,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    status_choices = [
        ('ordered','ordered'),
        ('confirmed','confirm'),
        ('delivered','deliver'),
        ('canceled','cancel'),
        
    ]
    status = models.CharField(
        max_length=10,
        choices=status_choices,
        default = 'ordered',
        
    )
    price = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    
    def __str__(self):
        return str(self.order_id)
    

    
    