from django.db import models

# Create your models here.


class DeletedEmployee(models.Model): 
    name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    photo = models.ImageField(
        upload_to='profiles',
        blank=True,
        null=True,
        default='img/profiles/avatar.png'
    )
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    date_hired = models.DateField(null=True, blank=True)
    
    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True)

    
    def __str__(self):
        if self.name:
            return f"Deleted Employee: {self.name}"
        return f"Deleted Employee: {self.phone_number or 'unknown'}"