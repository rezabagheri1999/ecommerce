from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from market.settings import AUTH_USER_MODEL
from django.conf import settings



User = get_user_model()
# Category

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])



# Product Color

class ProductColor(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7,help_text='Enter color hex code : ')

    def __str__(self):
        return self.name

# Product

class Product(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_colors = models.ManyToManyField(ProductColor, related_name='products', blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    def is_on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price

    def get_current_price(self):
        return self.discount_price if self.is_on_sale() else self.price


# PorductImage

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/images/')
    alt_text = models.CharField(max_length=100,blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured','created_at']


