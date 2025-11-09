from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from base.models import User, Product
from .models import DeletedEmployee
from .signals import backup_deleted_employee
from django.contrib import messages
from .froms import CreateEmployeeForm, CreateEmployeeProfile
from base.profiles import EmployeeProfile, POSITIONS_BY_DEPARTMENT, DEPARTMENT_CHOICES
from django.utils.safestring import mark_safe
import json
from base.decorators import allowed_roles
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
# Create your views here.


def _employees():
    users = User.objects.all()
    employees = []
    for user in users:
        if user.role == "employee":
            employees.append(user)
    return employees


def get_department(employee):
    current_department = []
    for dept in DEPARTMENT_CHOICES:
        if dept[0] == employee.employeeprofile.department:
            current_department = [dept[0], dept[1]]
    return current_department


def _total(model, keyword):
    return model.objects.aggregate(total=Sum(keyword))["total"] or 0


@allowed_roles(["manager"])
def home(request):
    if request.user.id != None:
        if request.user.role == "manager":
            employees = _employees()
            deleted_employees = DeletedEmployee.objects.all()
            total_sales = _total(Product, "sales_count")
            total_stock = _total(Product, "stock")
            total_price = _total(Product, "price")
            total_products = Product.objects.count()
            departments = []
            for department in DEPARTMENT_CHOICES:
                departments.append(department[0])
            context = {
                "employees": employees,
                "departments": departments,
                "deleted_employees": deleted_employees,
                "total_sales": total_sales,
                "total_stock": total_stock,
                "total_price": total_price,
                "total_products": total_products,
            }
            return render(request, "manager/index.html", context)
        elif request.user.role == "employee":
            messages.error(request, "Access Denied")
            return redirect("employee:home")
    messages.error(request, "Access Denied")
    return redirect("home")


@allowed_roles(["manager"])
def viewEmployee(request, id):
    employee = get_object_or_404(User, id=id)
    current_department = get_department(employee)
    current_position = POSITIONS_BY_DEPARTMENT[current_department[0]]
    context = {
        "no_search_bar": "no",
        "employee": employee,
        "current_department": current_department,
        "current_position": current_position,
    }
    return render(request, "manager/employee.html", context)


@allowed_roles(["manager"])
def deleteEmployee(request, id):
    employee = get_object_or_404(User, id=id)
    if request.method == "POST":
        if request.user.role == "manager":
            backup_deleted_employee(request.user, employee)
            employee.delete()
            messages.success(request, f"Employee {employee} Deleted Successfully")
        else:
            messages.error(request, "You Are Not Authorized")
        return redirect("manager:home")

    current_department = get_department(employee)
    current_position = POSITIONS_BY_DEPARTMENT[current_department[0]]
    context = {
        "no_search_bar": "no",
        "current_department": current_department,
        "current_position": current_position,
        "employee": employee,
    }
    return render(request, "manager/delete-employee.html", context)


@allowed_roles(["manager"])
def addEmployee(request):
    positions_json = json.dumps(POSITIONS_BY_DEPARTMENT)
    departments_json = json.dumps(DEPARTMENT_CHOICES)
    password2_help_text = False
    password2_error = False
    form = CreateEmployeeForm()
    profileForm = CreateEmployeeProfile()
    if request.method == "POST":
        form = CreateEmployeeForm(request.POST, request.FILES)
        profileForm = CreateEmployeeProfile(request.POST, request.FILES)
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")
        department = request.POST.get("department")
        position = request.POST.get("position")
        if form.is_valid() and profileForm.is_valid():
            if password1 == password2:
                # get instance form user form
                employee = form.save(commit=False)
                # set employee role
                employee.role = "employee"
                # set password
                employee.set_password(password1)
                # save new employee
                employee.save()

                # get data from input form
                instanceProfile = profileForm.save(commit=False)
                # get profile from database
                employeeProfile, created = EmployeeProfile.objects.get_or_create(
                    user=employee
                )

                employeeProfile.phone_number = instanceProfile.phone_number
                employeeProfile.address = instanceProfile.address
                employeeProfile.department = department
                employeeProfile.position = position
                employeeProfile.salary = instanceProfile.salary

                employeeProfile.save()
                messages.success(request, "User Created Successfully!")
                return redirect("manager:home")
            # passwords don't match
            else:
                messages.error(request, "Passwords Do Not Match")
        else:
            form = CreateEmployeeForm()
            profileForm = CreateEmployeeProfile()
            messages.error(request, "Data is not valid, Try Again!")
    context = {
        "form": form,
        "profileForm": profileForm,
        "password2_help_text": password2_help_text,
        "password2_error": password2_error,
        "positions_by_department_json": positions_json,
        "departments_json": departments_json,
    }
    return render(request, "manager/add-update-employee.html", context)


@allowed_roles(["manager"])
def updateEmployee(request, id):
    positions_json = json.dumps(POSITIONS_BY_DEPARTMENT)
    departments_json = json.dumps(DEPARTMENT_CHOICES)

    # Get employee and profile
    employee = get_object_or_404(User, id=id)
    employeeProfile = get_object_or_404(EmployeeProfile, user=employee)

    # Parse data to HTML
    form = CreateEmployeeForm(instance=employee)
    profileForm = CreateEmployeeProfile(instance=employeeProfile)

    # Handle POST request
    if request.method == "POST":
        Nform = CreateEmployeeForm(request.POST, request.FILES, instance=employee)
        NprofileForm = CreateEmployeeProfile(
            request.POST, request.FILES, instance=employeeProfile
        )

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("password_new")
        new_password2 = request.POST.get("password_new2")

        # Handle password update
        if old_password:
            if employee.check_password(old_password):
                if not new_password:
                    messages.error(request, "New password field is empty.")
                elif new_password != new_password2:
                    messages.error(request, "New passwords do not match.")
                else:
                    employee.set_password(new_password)
                    employee.save()
                    update_session_auth_hash(request, employee)  # Keeps user logged in
                    messages.success(
                        request,
                        mark_safe(
                            f"Employee <strong>{employee.username}</strong> password updated successfully!"
                        ),
                    )
            else:
                messages.error(
                    request, "Old password does not match the user password."
                )

        if Nform.is_valid():
            for name, new_value in Nform.cleaned_data.items():
                old_value = getattr(employee, name)
                if old_value != new_value:
                    setattr(employee, name, new_value)
            employee.save()
        else:
            pass

        if NprofileForm.is_valid():
            for namep, new_valuep in NprofileForm.cleaned_data.items():
                old_valuep = getattr(employeeProfile, namep)
                if old_valuep != new_valuep:
                    setattr(employeeProfile, namep, new_valuep)
            chosen_department = request.POST.get("department")
            chosen_position = request.POST.get("position")
            if chosen_department is not None and chosen_position is not None:
                employeeProfile.department = chosen_department
                employeeProfile.position = chosen_position
            employeeProfile.save()
        else:
            pass

        if Nform.is_valid() or NprofileForm.is_valid():
            form = Nform
            profileForm = NprofileForm
            messages.success(
                request,
                mark_safe(
                    f"Employee <strong>{employee.first_name} {employee.last_name}</strong> Updated Succesfully!"
                ),
            )
            return redirect("manager:home")

    current_department = get_department(employee)
    current_position = POSITIONS_BY_DEPARTMENT[current_department[0]]
    context = {
        "update": "update",
        "employee": employee,
        "form": form,
        "profileForm": profileForm,
        "current_department": current_department,
        "current_position": current_position,
        "positions_by_department_json": positions_json,
        "departments_json": departments_json,
    }

    return render(request, "manager/add-update-employee.html", context)


@allowed_roles(["manager"])
def allEmployees(request):
    context = {}
    employees = User.objects.filter(role='employee')
    if request.method == 'GET':
        q = request.GET.get('q') 
        if q:
            employees = User.objects.filter(
            Q(role='employee') and
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q))
            context['q'] = q
    grouped_employees = {}
    for dep in DEPARTMENT_CHOICES:
        dlist = []
        for employee in employees:
            if employee.employeeprofile.department == dep[0]:
                dlist.append(employee)
                # print(f'{employee} - {dep[0]}')
        # dlist.append(dep[0])

        grouped_employees[f'{dep[0]}'] = dlist

    
    context = {
        'grouped_employees': grouped_employees, 
        'page_title': 'Employees by Department', # Adjusted title to match content
        'current_view': 'all-employees',
        # 'q': q # Pass the search query back to the template for display/persistence
    }
    
    return render(request, 'manager/employees_list.html', context)

# def allEmployees(request):
#     employees = _employees()
#     from base.profiles import DEPARTMENT_CHOICES

#     departments = DEPARTMENT_CHOICES
#     context = {
#         "employees": employees,
#         "departments": departments,
#     }
#     return render(request, "manager/employees_list.html", context)
#     return render(request, "manager/all-employees.html", context)