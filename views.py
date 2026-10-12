from django.shortcuts import render,redirect
from .models import Menu
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        phone = request.POST.get('phone')

        cart_items = request.POST.get('cart_items')

        import json

        try:
            items = json.loads(cart_items)
        except (TypeError, ValueError):
            return render(request, 'checkout.html', {
                'error': 'Invalid cart details'
            })

        total = 0

        for item in items:
            product_id = item.get('id')
            quantity = item.get('quantity', 1)

            try:
                quantity = int(quantity)
                if quantity < 1:
                    raise ValueError

                product = Menu.objects.get(id=product_id)
                total += product.price * quantity

            except (Menu.DoesNotExist, ValueError, TypeError):
                return render(request, 'checkout.html', {
                    'error': 'Invalid product or quantity'
                })

        with connection.cursor() as cursor:
            cursor.execute(
                """
INSERT INTO orders
(customer_name, phone, total_amount, user_id)
VALUES (%s, %s, %s, %s)
                """,
                [name, phone, total, request.user.id]
            )

        return render(request, 'success.html')

    return render(request, 'checkout.html')



@login_required(login_url='/login/')
def my_orders(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, customer_name, phone,
                   total_amount, order_date
            FROM orders
            WHERE user_id = %s
            ORDER BY id DESC
        """, [request.user.id])

        orders = cursor.fetchall()

    return render(request, 'my_orders.html', {'orders': orders})




from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
def home(request):
    items = Menu.objects.all()
    return render(request, 'index.html', {'menu': items})

def cart(request):
    return render(request,'cart.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})