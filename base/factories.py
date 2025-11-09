import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from .models import Product, Category, User
from .profiles import ManagerProfile, EmployeeProfile, CustomerProfile
import random
from django.shortcuts import get_object_or_404
fake = Faker()


SMARTPHONE_WORDS = [
    "iPhone 15", "Galaxy S24", "Pixel 9", "OnePlus 12", "Xiaomi 14",
    "Asus ROG Phone 8", "Honor Magic6", "Redmi Note 13", "Realme GT5"
]

LAPTOP_WORDS = [
    "MacBook Air M3", "Dell XPS 15", "Lenovo ThinkPad X1", "HP Spectre x360",
    "Asus ZenBook 14", "Acer Swift 5", "MSI Stealth 16", "Razer Blade 18"
]

ACCESSORY_WORDS = [
    "AirPods Pro 2", "Galaxy Buds3 Pro", "Sony WH-1000XM5", "Logitech MX Master 3S",
    "Apple Magic Keyboard", "Anker PowerCore 10000", "Belkin BoostCharge Pro",
    "Razer BlackShark V2", "JBL Flip 7", "Sandisk Extreme Pro 1TB"
]

CAMERA_WORDS = [
    "Canon EOS R6 Mark II", "Sony Alpha A7 IV", "Nikon Z6 II", "Fujifilm X-T5",
    "Panasonic Lumix GH6", "Leica Q3", "Canon EOS R50", "Sony ZV-E10 II",
    "Olympus OM-D E-M10 IV", "GoPro Hero 12 Black"
]


class ProductFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Product
 
  category = factory.LazyFunction(lambda: random.choice(Category.objects.all())) 
   
  name = factory.LazyAttribute(
        lambda obj: fake.random_element(
            SMARTPHONE_WORDS if obj.category.name == "smartphones" else
            LAPTOP_WORDS if obj.category.name == "laptops" else
            ACCESSORY_WORDS if obj.category.name == "accessories" else
            CAMERA_WORDS
        )
    )

  company = factory.LazyAttribute(
        lambda obj: obj.name.split(' ', 1)[0]
    )
  price = factory.LazyAttribute(
     lambda obj: round( 
       random.uniform(400, 1500)
       if obj.category.name == "smartphones" else 
       random.uniform(700, 3000)
       if obj.category.name == "laptops" else 
       random.uniform(20, 300)
       if obj.category.name == "accessories" else 
       random.uniform(500, 4000)
       if obj.category.name == "cameras" else  0, 
       2
       )
  ) 
  
  description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
  discount = factory.LazyAttribute(lambda _: round(random.uniform(0,50)))
  stock = factory.LazyAttribute(lambda _: round(random.uniform(1,500)))
  is_hot_deal = factory.LazyAttribute(lambda obj: obj.discount > 25)  
  sales_count = factory.LazyAttribute(lambda _: round(random.uniform(0,1000)))
  rating = factory.LazyAttribute(lambda _: random.uniform(0,5))


class ManagerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ManagerProfile

    phone_number = factory.Faker('phone_number')
    office_location = factory.Faker('city')

class EmployeeProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeProfile

    phone_number = factory.Faker('phone_number')
    salary = factory.LazyAttribute(lambda _: round(random.uniform(2000,10000)))

class CustomerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerProfile

    phone_number = factory.Faker('phone_number')
    balance = factory.LazyAttribute(lambda _: round(random.uniform(0,2000)))
    coupons_count = factory.LazyAttribute(lambda _: round(random.uniform(0,20)))
    address = factory.Faker('city')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'user'
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.LazyFunction(lambda: make_password('user'))
    # keep default role small and canonical
    role = 'customer'
    


def create_users(count, index, oldid, username, oldrole):
  
  i = 0;
  
  while i <= count:
    newid = oldid + i
    newusername = f"{username}-{index}"
    UserFactory.create(id=newid, username=newusername, role=oldrole) 
    print(f"creating user {newusername} done!")
    index = index + 1
    i = i + 1
  
  print("Proccess Finished")
  
