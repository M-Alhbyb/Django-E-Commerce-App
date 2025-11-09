# 🛒 Django E-Commerce Platform

A modern, **full-featured E-Commerce solution** built with **Django** and **Python**. This platform is engineered for scalability and robustness, providing essential modules for product management, secure customer authentication, a dynamic shopping cart, and comprehensive order tracking.

This project serves as a clear demonstration of **robust backend logic**, **dynamic template rendering**, and a **clean, modular architecture** suitable for building a professional online store.

---

## ✨ Key Features & Demo

|         Feature          | Description                                                                                       |                               Demo Preview                               |
| :----------------------: | :------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------: |
|   👨‍💻 **User Accounts**    | Secure sign-up, login, profile management, and personalized user experience.                      |         ![User Demo](https://your-demo-video-link-here/user.gif)         |
|   🛍️ **Shopping Cart**    | Intuitive interface to add, remove, and update item quantities dynamically.                       |         ![Cart Demo](./demos/gifs/shopping-gallery.g)         |
|   ⚙️ **Admin Control**    | Comprehensive **Django Admin Dashboard** for managing products, orders, customers, and inventory. |        ![Admin Demo](https://your-demo-video-link-here/admin.gif)        |
|  🖼️ **Product Gallery**   | Dedicated management for product images and multi-image galleries.                                |      ![Gallery Demo](https://your-demo-video-link-here/gallery.gif)      |
|  🔎 **Search & Filter**   | Powerful product search and filtering options by category, department, or keywords.               |       ![Search Demo](https://your-demo-video-link-here/search.gif)       |
|  💰 **Dynamic Pricing**   | Logic to apply discounts, handle promotional codes, and manage product price variations.          |      ![Pricing Demo](https://your-demo-video-link-here/pricing.gif)      |
|   🧠 **Modular Design**   | Clean, scalable, and maintainable **Clean Django Architecture** using separate, decoupled apps.   | ![Architecture Demo](https://your-demo-video-link-here/architecture.gif) |
|   👤👤👤 **Separated Apps**   | Three different apps (**Normal User, Employee, And Manager**) with different permissions   | ![Separated Demo](https://your-demo-video-link-here/architecture.gif) |
|    **Full Data API**   | All project data (**Available as API**) handled by permissions  | ![API Demo](https://your-demo-video-link-here/architecture.gif) |

> 🎬 **Watch the Full Demo Video Here:**
> [![Demo Video](https://img.shields.io/badge/▶️%20Project%20Walkthrough-3498DB?style=for-the-badge&logo=youtube)](https://your-demo-video-link-here)

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
```
Bash

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

# .env file
SECRET_KEY=your_strong_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
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
    ├── serializers.py
    ├── views.py
    └── urls.py
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

## Author: Mohamed (Pasha)

    📧 Email: mohammedalhbyb@gmail.com

    🌐 Portfolio/LinkedIn: https://linkedin.com