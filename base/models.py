from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    photo = models.ImageField(upload_to='profiles', blank=True, null=True, default='img/profiles/avatar.png')
    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("employee", "Employee"),
        ("customer", "Customer"),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="customer")

class UserManager(models.Manager):
    def managers(self):
        return self.filter(role="manager")

    def employees(self):
        return self.filter(role="employee")

    def customers(self):
        return self.filter(role="customer")

class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    # -------------
    name = models.CharField(max_length=100, null=False, blank=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    photo = models.ImageField(upload_to='products', blank=False, null=False, default='products/default-product.png') 
    # -------------
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=1)
    # -------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # -------------
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    is_hot_deal = models.BooleanField(default=False)
        
    sales_count = models.PositiveIntegerField(default=0)
    
    rating = models.FloatField(default=0, validators=[
        MinValueValidator(0.0),  # optional, minimum value
        MaxValueValidator(5.0)   # maximum value
    ])
    
    @property
    def old_price(self):
        return self.price + (self.discount * self.price / 100)
   
    @property
    def half_star(self):
        if self.rating % 1 == 0:
            return False
        else:
            return True
        
    @property
    def stars(self):
        full = int(self.rating) 
       
        if self.rating % 1 == 0:
            half = 0
        else:
            half = 1
        
        empty = 5 - full - half
        
        return {'full':full, 'half':half, 'empty':empty}
    
    def __str__(self):
        return self.name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='products/gallery', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    class Meta:
        verbose_name = 'Images Gallery'
        verbose_name_plural = 'Images Gallerys'

    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    
    def __str__(self):
        return f"{self.user.username}'s cart"
    
    # TODO related name
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product} x {self.quantity}"
    