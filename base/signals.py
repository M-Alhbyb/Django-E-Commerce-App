from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.apps import apps
from django.db.models.signals import post_save
from .models import User
from .profiles import ManagerProfile, EmployeeProfile, CustomerProfile


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    if sender.name == "accounts":
        groups = ["Manager", "Employee", "Customer"]
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            Product = apps.get_model("base", "Product")
            can_add = Permission.objects.get(codename="add_product")
            can_change = Permission.objects.get(codename="change_product")
            can_delete = Permission.objects.get(codename="delete_product")
            employee_group = Group.objects.get(name="Employee")
            employee_group.permissions.set([can_add, can_change, can_delete])


def create_employee(username, password):
    user = User.objects.create_user(
        username=username, password=password, role="employee"
    )
    group = Group.objects.get(name="Employee")
    user.groups.add(group)
    return user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "manager":
            ManagerProfile.objects.create(user=instance)
        elif instance.role == "employee":
            EmployeeProfile.objects.create(user=instance)
        elif instance.role == "customer":
            CustomerProfile.objects.create(user=instance)
