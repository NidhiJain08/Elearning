from django.shortcuts import render, redirect 
from django.views.decorators.csrf import csrf_exempt
import razorpay
from courses.models import Course
def home(request):
     return render(request, 'index.html')

def pay_with_razor(request,slug):
     if request.method=='POST':
      client = razorpay.Client(auth=("KEY_ID", "SECRET_KEY"))

      client.order.create({
  "amount": 50000,
  "currency": "INR",
  "payment_capture":'1',
  "notes": {
    "address": "udaipur"
  }
})
     context = {'slug':slug}
     return render (request,'pay_index.html',context)

@csrf_exempt
def success(request,slug):
     this_course = Course.objects.get(slug=slug)
     return render(request,"success.html")