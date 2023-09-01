from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

#model for storind the user's location
class User_details(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key = True,
        
        )
    mobile = models.BigIntegerField(default=0)
    village = models.CharField(max_length=50)
    city = models.CharField(max_length = 50)
    mandal = models.CharField( max_length=50)
    district = models.CharField( max_length=50)
    state = models.CharField( max_length=50)
    country = models.CharField( max_length=50)
    pin = models.CharField(max_length=8)
    latitude = models.DecimalField( default = 0,max_digits = 20,decimal_places= 10)
    longitude = models.DecimalField(default=0, max_digits=20,decimal_places= 10)
    seller_id = models.CharField(
        max_length = 20,
    
        )
    
    rating = models.IntegerField(default = 5)
    

    
    def __str__(self):
        return  self.user.username 
    
class Qr(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True,
    )
    key = models.CharField(max_length = 64,)
    qr = models.ImageField( upload_to ='qr/',)
    
    def __str__(self):
        return self.user.username    
    

    
    

