# -*- coding: utf-8 -*-

from .models import product,Productattribute
from django.db.models import Min,Max

def get_filters(request):
    cat=product.objects.distinct().values('category__title','category__id')
    brand=product.objects.distinct().values('brand__title','brand__id')
    sizes=Productattribute.objects.distinct().values('size__size','size__id')
    color=Productattribute.objects.distinct().values('color__color_code','color__color_title','color__id')
    minmaxprice=Productattribute.objects.aggregate(Min('price'),Max('price'))
    
    data={
        'cats':cat,
        'brands':brand,
        'colors':color,
        'sizes':sizes,
        'minMaxPrice':minmaxprice
        }
    return data    
    