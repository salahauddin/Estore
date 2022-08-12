from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class Brand(models.Model):
    title=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural='1. Brand'
        
    def __str__(self):
        return self.title
    
    
class category(models.Model):
    title=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural='2. Categories'
        
    def __str__(self):
        return self.title
        
    

    
    
class color(models.Model):
    color_code=models.CharField(max_length=15)
    color_title=models.CharField(max_length=15)
    class Meta:
        verbose_name_plural='4. Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.color_title
    
class Sizes(models.Model):
    size=models.CharField(max_length=15)
    class Meta:
        verbose_name_plural='5.Sizes'
        
    def __str__(self):
        return self.size
    
class product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=400,default="a")
    description=models.TextField()
    category=models.ForeignKey(category,on_delete=models.CASCADE,default="Free")
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    isFeatured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='3. Products'

    def __str__(self):
        return self.title

class Productattribute(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    color=models.ForeignKey(color,on_delete=models.CASCADE)
    size=models.ForeignKey(Sizes,on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural='6.Product Attributes'
        
    def __str__(self):
        return self.product.title

