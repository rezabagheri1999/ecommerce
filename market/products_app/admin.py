from django.contrib import admin
from .models import Category,Product,ProductColor,ProductImage
# Register your models here.

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ('name','is_active')
    prepopulated_fields = {'slug':('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','stock','is_active')
    list_filter = ('category','is_active','is_featured')
    search_fields = ('name','description')
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductImageInline]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductColor)
admin.site.register(ProductImage)


