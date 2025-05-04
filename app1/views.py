from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from app1.forms import UploadForm
from django.conf import settings
import os
from pathlib import Path
from app1.yolov5_detector import detect_objects  # Import YOLOv5 detector

# Create your views here.

@csrf_exempt
def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Automatically log the user in after signing up
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass') 
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!")
        
    return render (request,'login.html')


def video_analysis(request):
    return render(request, 'video_analysis.html')


# IMAGE ANALYSIS FUNCTION
def analyze_image(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        upload_path = f'media/uploads/{image.name}'

        # Save image
        with open(upload_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Run YOLOv5 detection
        detections = detect_objects(upload_path)

        context = {
            'image_url': upload_path,
            'detections': detections,
        }

    return render(request, 'image_analysis.html', context)


# IMAGE UPLOAD FUNCTION
def image_upload(request):
    if request.method == 'POST' and request.FILES.get('upload_image'):
        image = request.FILES['upload_image']
        
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(image.name, image)
        
        # Store path to display image in template using MEDIA_URL
        request.session['uploaded_image'] = f'uploads/{filename}'
        return redirect('analyze_image')  # Adjust this to use analyze_image view

    return redirect('image_analysis')


# LOGOUT FUNCTION
def Logoutview(request):
    logout(request)
    return redirect('login')
