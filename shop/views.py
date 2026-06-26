from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

from .models import Cart,Order
from courses.models import *
from users.models import *

@login_required(login_url='users:signup')
def all_courses(request):
    user = request.user
    if request.method =='POST':
        title = request.POST.get('title').strip()
        student_courses =  [table.course for table in Student_course.objects.filter(student = request.user)] 
        cart_courses =  [table.course for table in Cart.objects.filter(user = request.user)] 
        extra_courses =  user.extra_courses.all()
        all_courses = Course.objects.filter(title__icontains=title,ready=True)
    else:
        student_courses =  [table.course for table in Student_course.objects.filter(student = request.user)] 
        cart_courses =  [table.course for table in Cart.objects.filter(user = request.user)] 
        extra_courses =  user.extra_courses.all()
        all_courses = Course.objects.filter(ready=True)
    return render(request,'all_courses.html',{'all_courses':all_courses,'student_courses':student_courses,'cart_courses':cart_courses,'extra_courses':extra_courses})

@login_required(login_url='users:signup')
def my_cart(request):
    my_courses = Cart.objects.filter(user=request.user)
    money=0
    for i in my_courses:
        money+=i.total_price()
    return render(request,'my_cart.html',{'my_courses':my_courses,'money':money})


@login_required(login_url='users:signup')
@require_POST
def add_cart(request,course_id):
    course=Course.objects.get(id=course_id)
    cart = Cart.objects.filter(user=request.user,course=course).first()
    if cart !=None:
        return JsonResponse({'status': 'have', 'course_id': course_id})
    else:
        cart = Cart.objects.create(user=request.user,course=course)
        return JsonResponse({'status': 'ok', 'course_id': course_id})

@login_required(login_url='users:signup')
def delete_cart(request,course_id):
    course = Course.objects.get(id=course_id)
    cart = Cart.objects.filter(user=request.user,course=course).first()
    cart.delete()
    return redirect('shop:my_cart')
    



@login_required(login_url='users:signup')
def create_order(request):
    user = request.user
    cart_items  = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('shop:my_cart')
    total_amount:int = 0 
    for i in cart_items:
        total_amount+= i.total_price()
    order = Order.objects.create(user=user,email=user.email,total_amount=total_amount)
    return redirect('shop:create_checkout_session',order_id=order.id)

def create_checkout_session(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    line_item = {
        'price_data':{
            'currency':'kzt',
            'unit_amount':int(order.total_amount * 100),
            'product_data':{
            'name': f'Заказ  №{order.id}'
        }
        },
        
        'quantity':1
    }
    cancel_url = request.build_absolute_uri(reverse('shop:stripe_cancel',args=[order.id]))
    succces_url = request.build_absolute_uri(reverse('shop:stripe_success',args=[order.id]))
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[line_item],
            mode='payment',
            success_url = succces_url,
            cancel_url = cancel_url
        )
        order.stripe_id = checkout_session.id
        order.save()
        return redirect(checkout_session.url,code = 303)
    except Exception as e:
        print(e)
        return redirect('shop:my_cart')

def stripe_success(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    session_id = order.stripe_id
    if not session_id:
        messages.error(request, 'Stripe session not found')
        return redirect('shop:my_cart')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            order.status = 'paid'
            order.save()
            objects = Cart.objects.filter(user=order.user)
            for obj in objects:
                Student_course.objects.create(student=order.user,course=obj.course)
            objects.delete()
            messages.success(request, 'Payment successful')
            return redirect('shop:all_courses')
        else:
            messages.warning(request, 'Payment not completed')
            return redirect('shop:my_cart')
    except Exception as e:
        print(e)
        messages.error(request, 'Stripe error')
        return redirect('shop:my_cart')
    
def stripe_cancel(request,order_id):
    order = get_object_or_404(Order,id=order_id)
# сбросить статус заказа
    session_id = order.stripe_id
    if not session_id:
        messages.error(request, 'Stripe session not found')
        return redirect('shop:my_cart')
    else:
        order.status = 'created'
        order.save()
        messages.info(request, 'Payment canceled')
        return redirect('shop:all_courses') 