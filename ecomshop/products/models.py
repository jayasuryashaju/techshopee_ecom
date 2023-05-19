from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=50, null=True)
    image1 = models.ImageField(upload_to='products/', null=True, blank=True)
    image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    image3 = models.ImageField(upload_to='products/', null=True, blank=True)
    image4 = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=False)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to='banners')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Banner {self.id}"
