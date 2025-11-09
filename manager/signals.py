from .models import DeletedEmployee

def backup_deleted_employee(manager, instance, **kwargs):
  DeletedEmployee.objects.create(
    name = instance.username,
    first_name = instance.first_name,
    last_name = instance.last_name,
    email = instance.email,         
    photo = instance.photo,
    phone_number = instance.employeeprofile.phone_number,
    address = instance.employeeprofile.address,
    salary = instance.employeeprofile.salary,
    position = instance.employeeprofile.position,
    department = instance.employeeprofile.department,
    date_hired = instance.employeeprofile.date_hired,
    deleted_by = manager
      )  
  print('Creation Done')
         
         
         
         
        
         
         