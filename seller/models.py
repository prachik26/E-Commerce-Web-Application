from PIL import Image
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Seller(models.Model):
    user=models.OneToOneField(User,max_length=60, blank=True,unique=True, on_delete=models.CASCADE)
    fname=models.CharField(max_length=60, blank=True)
    email=models.EmailField(max_length=60, blank=True)
    comp_name=models.CharField(max_length=60, unique=True, blank=True)
    password=models.CharField(max_length=60, blank=True)
    
    def __str__(self):
        return self.comp_name

class Product(models.Model):
    prodname=models.CharField(max_length=100, blank=True)
    shop=models.ForeignKey(Seller, max_length=100, blank=True,null=True, on_delete=models.SET_NULL)
    desc=models.CharField(max_length=70, blank=True, null=True)
    price = models.FloatField()
    prodimg = models.ImageField(upload_to="product",default="",null=True, blank=True)

    def __str__(self):
        return self.prodname

    @property
    def imageURL(self):
        try:
            url = self.prodimg.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.prodimg.path)
        if img.height > 1500 or img.width > 1500:
            output_size = (1500, 1500)
            img.thumbnail(output_size)
            img.save(self.prodimg.path)