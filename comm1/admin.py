from django.contrib import admin
from .models import Brand,category,product,Sizes,color,Productattribute

# Register your models here.

admin.site.register(Brand)


admin.site.register(category)

class Products(admin.ModelAdmin):
        list_display=('id','title','description','status','brand','category','isFeatured','slug')
        list_editable=('title','description','status','isFeatured')
admin.site.register(product,Products)

class ProductAttributes(admin.ModelAdmin):
        list_display=('id','product','color','size','price')
admin.site.register(Productattribute,ProductAttributes)


class Colors(admin.ModelAdmin):
        list_display=('color_title','color_bg')
admin.site.register(color,Colors)


admin.site.register(Sizes)








