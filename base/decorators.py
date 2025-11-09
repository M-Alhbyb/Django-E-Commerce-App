# base/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def allowed_roles(roles=None):
    if roles is None:
        roles = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Step 1: Check authentication
            if not request.user.is_authenticated:
                messages.error(request, "Please log in first.")
                return redirect("login")

            # Step 2: Check role authorization
            if request.user.role not in roles:
                role = request.user.role
                messages.error(request, "Access Denied.")

                # Redirect to the user's own dashboard
                if role in ["employee", "manager"]:
                    return redirect(f"{role}:home")  # example: manager:home
                return redirect("home")

            # Step 3: All good — continue to the view
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
