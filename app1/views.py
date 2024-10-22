from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
# Create your views here.
from django.shortcuts import render
from .models import Product, Order
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
def register(request):
    form = UserCreationForm()
   
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
    contex={'form':form}    
    return render(request,'app/register.html',contex)
def home(request):
    sort_option = request.GET.get('sort', 'default')  # Lấy tùy chọn sắp xếp từ query string
    products = Product.objects.all()  # Lấy tất cả sản phẩm

    # Sắp xếp sản phẩm theo tùy chọn
    if sort_option == 'low_to_high':
        products = products.order_by('price')  # Sắp xếp từ thấp đến cao
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')  # Sắp xếp từ cao đến thấp

    # Phân trang sản phẩm, hiển thị 8 sản phẩm mỗi trang
    paginator = Paginator(products, 8)  # Hiển thị 8 sản phẩm mỗi trang
    page_number = request.GET.get('page')  # Lấy số trang từ query string
    page_obj = paginator.get_page(page_number)

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_paid=False)
        cart_item_count = order.orderitem_set.count()  # Lấy số lượng item trong giỏ hàng
    else:
        cart_item_count = 0  # Nếu người dùng chưa đăng nhập, giỏ hàng sẽ là 0

    # Tạo context cho template
    context = {
        'page_obj': page_obj,  # Sử dụng `page_obj` để lấy danh sách sản phẩm trong template
        'cart_item_count': cart_item_count,
        'sort_option': sort_option  # Để giữ lại tùy chọn sắp xếp trên các trang
    }
    
    return render(request, "app/home.html", context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_paid=False)
        items = order.orderitem_set.all()

        total_price = 0  # Khởi tạo giá trị tổng
        
        for item in items:
            # Tính tổng giá cho mỗi OrderItem
            item.total_price = float(item.get_total())
            total_price += item.total_price  
            print( {item.get_total()})
    else:
        items = []
        
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        total_price = 0

    context = {'items': items, 'order': order, 'total': total_price}
    print("check", items)
    return render(request, "app/cart.html", context)

def updateItems(request):
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')
    quantity = data.get('quantity')  # Lấy số lượng mới nếu có
    
    # Kiểm tra kiểu dữ liệu của quantity
    if quantity is not None and not isinstance(quantity, int):
        return JsonResponse({'error': 'Invalid quantity. Must be an integer.'}, status=400)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, is_paid=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'update':
        if quantity is not None and quantity >= 0:  # Kiểm tra giá trị quantity
            orderItem.quantity = quantity  # Cập nhật số lượng mới
        else:
            return JsonResponse({'error': 'Invalid quantity value. Must be a non-negative integer.'}, status=400)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    if orderItem.quantity > 0:
        total_price = orderItem.quantity * orderItem.product.price
    else:
        total_price = 0

    order_total = sum(item.quantity * item.product.price for item in order.orderitem_set.all())

    return JsonResponse({
        'quantity': orderItem.quantity if orderItem.quantity > 0 else 0,
        'total_price': total_price,
        'order_total': order_total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('OrderItem', {})
    
    # Kiểm tra xem sản phẩm có trong giỏ hàng không
    if product_id in cart:
        del cart[product_id]  # Xóa sản phẩm khỏi giỏ hàng

    request.session['OrderItem'] = cart  # Cập nhật giỏ hàng trong session
    return redirect('cart_view')  # Chuyển hướng về trang giỏ hàng


# views.py
def cart_view(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, is_paid=False)
    order_items = order.orderitem_set.all()

    for item in order_items:
        item.total_price = item.quantity * item.product.price

    context = {
        'order_items': order_items,
    }
    return render(request, 'cart.html', context)
