from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from premailer import transform
import os
from django.conf import settings
from base.models import User, Cart, CartItem
from django.shortcuts import get_object_or_404


def load_css(filename):
    path = os.path.join(settings.BASE_DIR, "static/css", filename)
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return ""


@shared_task
def send_checkout_email(id):
    user = get_object_or_404(User, id=id)
    name = f"{user.first_name} {user.last_name}"
    customer_email = user.email 
    cart = get_object_or_404(Cart, user=user)

    total_price = 0
    for item in CartItem.objects.all():
        total_price += item.product.price * item.quantity

    cart_items = []
    for item in CartItem.objects.all():
        if item.cart == cart:
            cart_items.append(item)
    
    context = {
        "name":name,
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
        "nofooter": True}
    
    html = render_to_string("base/checkout_email.html", context)

    bootstrap = load_css("bootstrap.min.css")
    slick = load_css("slick.css")
    slick_theme = load_css("slick-theme.css")
    nouislider = load_css("nouislider.min.css")
    fontawesome = load_css("font-awesome.min.css")
    custom = load_css("style.css")

    # Combine all CSS inside <style> block
    combined_css = bootstrap + slick + slick_theme + nouislider + fontawesome + custom

    html_with_css = f"<style>{combined_css}</style>" + html
    html_inlined = transform(html_with_css)

    subject = "Confirm Products Order"
    from_email = "Electro Store"

    try:
        msg = EmailMultiAlternatives(
            subject,
            "",
            from_email,
            [customer_email],
        )
        msg.attach_alternative(html_inlined, "text/html")
        msg.send()
    except Exception as e:
        return False
