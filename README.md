# 🛒 Django E-Commerce Platform

A modern, full-featured E-Commerce solution built with Django and Python. This platform is engineered for scalability and robustness, providing essential modules for product management, secure customer authentication, a dynamic shopping cart, and comprehensive order tracking.

This project serves as a clear demonstration of robust backend logic, dynamic template rendering, and a clean, modular architecture suitable for building a professional online store.

# Live Preview:
   [Live Preview](https://django-e-commerce-app-34ro.onrender.com)


# ✨ Key Features

   1. ***Secure User Accounts:*** Implements secure sign-up, login, password management, and personalized user profile management.
        
        ![User Account Demo](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/user-accounts.gif)

   2. ️***Dynamic Shopping Cart:*** Provides an intuitive interface to add, remove, and dynamically update item quantities for both authenticated and anonymous users.
        
        
        ![Shopping Cart Demo](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/shopping-cart.gif)

   3. ***Comprehensive Product Gallery:*** Dedicated management for main product images and support for multi-image galleries, enhancing the shopping experience.

        ![Product Gallery](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/product-gallery.gif)

   4. ***Advanced Search & Filtering:*** Powerful product search capabilities and filtering options by category, department, or keywords to help users quickly find products.

        ![Search & Filter Demo](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/search-filter.gif)

   5. ***Modular and Scalable Design:*** Utilizes a Clean Django Architecture with separate, decoupled applications for maximum maintainability and scalability.
   6. ***Role-Based Access Control (RBAC):*** Features distinct, separated applications and permissions for Normal Users, Employees, and Managers.
      
      1. **Anonymous User App**:


         ![anonymous](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/anonymous-user.gif)


      2. **Customer App**: 


          ![customer](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/user-accounts.gif)


      3. **Employee App**:  


          ![employee](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/employee-app.gif)


      4. **Manager App**: 
          
          
          ![manager](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/manager-app.gif)

          
   1. ***Full Data API (RESTful):*** All project data is exposed via a well-structured API, with access controlled by user permissions, enabling integration with mobile or external applications.  
   ![API Demo](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/gifs/api.gif)


> 🎬 **Watch the Full Demo Video Here:**

> [![Demo Video](https://img.shields.io/badge/▶️%20Project%20Walkthrough-3498DB?style=for-the-badge&logo=youtube)](https://github.com/M-Alhbyb/Django-E-Commerce-App/raw/main/demos/full)




---


## 🛠️ Technology Stack


| Category          | Tools                                          | Rationale                                                                                  |
| :---------------- | :--------------------------------------------- | :----------------------------------------------------------------------------------------- |
| **Backend**       | **Python**, **Django**                         | Robust, secure, and rapid development framework.                                           |
| **Database**      | **PostgreSQL** (Default)                       | Reliable and scalable for production environments. *Easily switchable to SQLite or MySQL.* |
| **Frontend**      | HTML5, CSS3, **Bootstrap**                     | Responsive design and quick styling.                                                       |
| **Key Libraries** | **Pillow**, **Django Admin**, **Font Awesome** | Image handling, powerful dashboard, and iconography.                                       |


---


## 🚀 Quick Start Guide


### Prerequisites


* Python 3.8+

* Git


### 1. Clone the Repository


```bash

git clone [https://github.com/m-alhbyb/ecommerce-project.git](https://github.com/m-alhbyb/ecommerce-project.git)

cd ecommerce-project

```


### 2. Set Up Environment & Dependencies

```Bash


# Create and activate a virtual environment

python -m venv venv

source venv/bin/activate # For Linux/macOS

# OR: venv\Scripts\activate # For Windows


# Install all required packages

pip install -r requirements.txt

```


### 3. Configure Environment Variables


Create a file named .env in the project root directory and add your secret credentials:

```Bash


# /etc/config.json

create /etc/config.json or edit settings.py
the file must contains 'SECRET_KEY' and 'EMAIL_HOST_USER' and 'EMAIL_HOST_PASSWORD'

# Add Database, Email, or Third-Party API keys here (e.g., PAYPAL_CLIENT_ID)

```


### 4. Database Setup & Launch

```Bash


# Run migrations to set up the database schema

python manage.py migrate


# (Optional) Create an administrative user

python manage.py createsuperuser


# Start the development server

python manage.py runserver

# Or Use Gunicorn (Best Practice)
source venv/bin/activate
gunicorn projectname.wsgi:application --bind 0.0.0.0:8000

Open your browser and navigate to: 👉 http://localhost:8000

```


## 🗂️ Project Architecture


The project is structured into modular Django applications for maximum maintainability and separation of concerns:

```ecommerce/

├── manage.py

├── requirements.txt

├── README.md

├── ecommerce/             # Project settings

│   ├── settings.py

│   ├── urls.py

│   └── wsgi.py

├── base/                  # Main app

│   ├── models.py

│   ├── views.py

|   ├── urls.py

|   └── ...

├── employee/              # Employee app

│   ├── views.py

|   ├── urls.py

|   └── ...

├── manager/               # Manager app

│   ├── views.py

|   ├── urls.py

|   └── ...

└── api/               # API app

|   ├── serializers.py

|   ├── views.py

|   └── urls.py

```


## 💡 Planned Enhancements


    ✅ Payment Gateway Integration: Implement secure payment processing via Stripe and/or PayPal.


    ✅ RESTful API: Develop a comprehensive API using Django REST Framework for mobile app support.


    ✅ I18n/L10n: Add multi-language and multi-currency support.


    ✅ User Experience: Introduce product reviews, ratings, and recommendation logic.


## 🤝 Contribution


Contributions are welcome! If you have suggestions, feature ideas, or bug fixes, please feel free to open an issue or submit a pull request.


## 📜 License


This project is open-source and released under the MIT License.


## 💬 Connect


## Author: Mohamed Alhbyb


    📧 Email: mohammedalhbyb@gmail.com


    🌐 Portfolio/LinkedIn: www.linkedin.com/in/mohamed-alhbyb
