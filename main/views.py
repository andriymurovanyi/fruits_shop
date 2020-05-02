from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Category, Product, Order, Client
from django.views.decorators.http import require_POST
from .helpers.cart import Cart
from .forms import CartAddProductForm
import json


def index(request):
    category = None

    category_id = request.GET.get('category_id')
    categories = Category.objects.all()
    query = request.GET.get('query')

    products = Product.objects.filter(available=True)

    if category_id:
        category = get_object_or_404(Category, pk=int(category_id))
        products = products.filter(category=category)

    if query:
        category = None
        products = products.filter(name__contains=query)

    template_url = 'main/pages/products.html'
    context = {
        'category': category,
        'categories_list': categories,
        'products_list': products,
    }

    return render(request, template_url, context)


def product(request, product_id):
    product_object = get_object_or_404(Product, pk=product_id)

    template_url = 'main/pages/product.html'
    context = {
        'product': product_object,
        'hide_search': True
    }

    return render(request, template_url, context)


def cart_page(request):
    cart = Cart(request)
    items = []

    product_ids = cart.details.keys()
    products = Product.objects.filter(id__in=product_ids)

    for i in range(len(products)):
        product_item = products[i].as_json
        product_item.update({
            'id': products[i].id,
            'quantity': cart.details[str(products[i].id)]['quantity']
        })
        items.append(product_item)

    template_url = 'main/pages/cart.html'
    context = {
        'cart': items,
        'total_price': cart.get_total_price(),
        'cart_length': len(cart),
        'hide_search': True,
        'hide_footer': True
    }

    return render(request, template_url, context)


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product_object = get_object_or_404(Product, id=product_id)

    form = CartAddProductForm(request.POST)

    if form.is_valid():

        cd = form.cleaned_data
        cart.add(product=product_object,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return HttpResponse(json.dumps({
        'status': 200,
        'product': product_object.as_json,
        'cart_length': len(cart)
    }), content_type='application/json')


@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)

    product_object = get_object_or_404(Product, id=product_id)
    cart.remove(product_object)

    return HttpResponse(json.dumps({
        'product': product_object.as_json,
        'cart_length': len(cart),
        'total_price': str(cart.get_total_price())
    }), content_type='application/json')


@require_POST
def make_order(request):
    cart = Cart(request)

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone_number = request.POST.get('phone_number')
    email = request.POST.get('email')
    city = request.POST.get('city')
    address = request.POST.get('address')
    total_price = cart.get_total_price()

    if not first_name or not phone_number or not city or not address:
        return HttpResponse(json.dumps({
            'error_message': 'This field is required'
        }))

    client = Client(first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    email=email)
    client.save()

    product_ids = cart.details.keys()
    products = Product.objects.filter(id__in=product_ids)

    order = Order(city=city,
                  address=address,
                  total_price=total_price,
                  client_id=client.id)
    order.save()

    for product_obj in products:
        order.products.add(product_obj)

    cart.clear()

    return redirect('main:cart_page')


def cart_details(request):
    cart = Cart(request)

    return HttpResponse(json.dumps({
        'status': 200,
        'cart_length': len(cart),
        'cart_details': cart.details
    }), content_type='application/json')
