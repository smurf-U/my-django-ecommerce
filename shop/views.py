import  json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Order, OrderLines, Customer
from .forms import AddressForm

def shop(request):
    context = {}
    5/0
    products = Product.objects.filter(sale_ok=True, active=True)
    res = getCart(request)
    context.update({'products': products})
    context.update(res)
    return render(request, 'shop/shop.html', context)

def cart(request):
    context = getCart(request)
    return render(request, 'shop/cart.html', context)

def checkout(request):
    context = getCart(request)
    return render(request, 'shop/checkout.html', context)

def checkoutAddress(request):
    context = getCart(request)
    return render(request, 'shop/address.html', context)

def updateAddress(request, id):
    context = getCart(request)
    customer = get_object_or_404(Customer, pk=id)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('/checkout')
    else:
        form = AddressForm(instance=customer)
    context.update({'form': form})
    return render(request, 'shop/address_edit.html', context)

def addInvoiceAddress(request):
    context = getCart(request)
    invoice_address = addAddress(request, type='invoice')
    if invoice_address.get('customer'):
        order = context.get('order')
        order.invoice_address_id = invoice_address.get('customer')
        order.save()
        return redirect('/checkout')
    context.update(invoice_address)
    return render(request, 'shop/address_edit.html', context)

def addShippingAddress(request):
    context = getCart(request)
    shipping_address = addAddress(request, type='delivery')
    if shipping_address.get('customer'):
        order = context.get('order')
        order.shipping_address_id = shipping_address.get('customer')
        order.save()
        return redirect('/checkout')
    context.update(shipping_address)
    return render(request, 'shop/address_edit.html', context)

def addAddress(request, type):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.parent_id = request.user.customer
            customer.type = type
            customer.save()
            return {'customer': customer}
    else:
        form = AddressForm()
    return {'form': form}

def updateCart(request, **kwarg):
    data = json.loads(request.body)
    customer = request.user.customer
    product, created = Product.objects.get_or_create(id=int(data.get('product')))
    order, created = Order.objects.get_or_create(customer_id=customer, state='draft')
    orderline, created = OrderLines.objects.get_or_create(order_id=order, product_id=product)
    if data.get('action') == 'add':
        orderline.product_qty += data.get('qty')
    else:
        orderline.product_qty -= data.get('qty')
    orderline.save()
    if orderline.product_qty <= 0:
        orderline.delete()
    return JsonResponse('', safe=False)

def updateOrderAddress(request, **kwarg):
    data = json.loads(request.body)
    customer = request.user.customer
    newAddress = Customer.objects.get(id=int(data.get('addressId')))
    order, created = Order.objects.get_or_create(customer_id=customer, state='draft')
    if data.get('type') == 'ship':
        print(newAddress)
        order.shipping_address_id = newAddress
    else:
        order.invoice_address_id = newAddress
    order.save()
    return JsonResponse('', safe=False)

def getCart(request):
    if request.user.is_authenticated and hasattr(request.user, 'customer'):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer_id=customer, state='draft')
        lines = order.orderlines_set.all()
        cartQuantity = int(order.getQuantity)
    else:
        lines = []
        order = {'getTotal':0 ,'getQuantity':0}
        cartQuantity = int(order['getQuantity'])

    return {'lines': lines, 'order':order, 'cartQuantity': cartQuantity}
