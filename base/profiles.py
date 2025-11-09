from django.db import models
from django.conf import settings

# --- Define department choices ---
DEPARTMENT_CHOICES = (
    ('management', 'Management'),
    ('sales', 'Sales'),
    ('marketing', 'Marketing'),
    ('customer_service', 'Customer Service'),
    ('product', 'Product Management'),
    ('logistics', 'Logistics & Supply Chain'),
    ('finance', 'Finance & Accounting'),
    ('hr', 'Human Resources'),
    ('it', 'Information Technology'),
    ('general', 'General'),
)

# --- Define positions for each department ---
POSITIONS_BY_DEPARTMENT = {
    'management': ['General Manager', 'Operations Manager', 'Assistant Manager'],
    'sales': ['Sales Executive', 'Account Manager', 'Business Development Associate'],
    'marketing': ['Digital Marketing Specialist', 'SEO Analyst', 'Social Media Manager'],
    'customer_service': ['Customer Support Representative', 'Live Chat Agent', 'Customer Experience Supervisor'],
    'product': ['Product Manager', 'Product Analyst', 'Merchandising Specialist'],
    'logistics': ['Logistics Coordinator', 'Inventory Controller', 'Delivery Supervisor'],
    'finance': ['Accountant', 'Financial Analyst', 'Billing Specialist'],
    'hr': ['HR Manager', 'Recruitment Officer', 'Training & Development Coordinator'],
    'it': ['Backend Developer', 'System Administrator', 'Technical Support Engineer'],
    'general': ['Administrative Assistant', 'Office Coordinator', 'Data Entry Clerk'],
}

# --- Build POSITIONS_CHOICES for Django field ---
POSITIONS_CHOICES = [
    (f"{dept}:{pos}", f"{pos} ({dict(DEPARTMENT_CHOICES)[dept]})")
    for dept in POSITIONS_BY_DEPARTMENT
    for pos in POSITIONS_BY_DEPARTMENT[dept]
]

# -------------------- Models --------------------

class ManagerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Manager: {self.user.username}"


class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    salary = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    date_hired = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=20, default='Active')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='general'
    )

    position = models.CharField(
        max_length=100,
        choices=POSITIONS_CHOICES,
        default='general:Administrative Assistant'
    )

    def __str__(self):
        return f"Employee: {self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    coupons_count = models.PositiveIntegerField(default=0)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.user.username}"

