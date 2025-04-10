from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from app1.forms import UploadForm
from django.conf import settings
from pathlib import Path
from app1.yolo_inference import detect_from_image
import os
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


def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Password and Confirm password are not same!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        

    return render (request,'signup.html')

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
def image_analysis(request):
    uploaded_image = request.session.get('uploaded_image')

    # Case: Show uploaded image
    if uploaded_image:
        image_url = uploaded_image
    else:
        # Fall back to dataset cycling
        DATASET_DIR = os.path.join(settings.BASE_DIR, 'static', 'images', 'dataset')

        image_list = sorted([
            f for f in os.listdir(DATASET_DIR)
            if f.lower().endswith(('.jpg', '.png', '.jpeg'))
        ])

        if not image_list:
            return render(request, 'image_analysis.html', {'error': 'No images found'})

        if 'image_index' not in request.session:
            request.session['image_index'] = 0
        else:
            if 'next' in request.GET:
                request.session['image_index'] += 1
                if request.session['image_index'] >= len(image_list):
                    request.session['image_index'] = 0

        image_index = request.session['image_index']
        current_image = image_list[image_index]
        image_url = f'images/dataset/{current_image}'

    # Dummy detection values (replace later with YOLO output)
    context = {
        'image_url': image_url,
    'is_uploaded': uploaded_image is not None,   
    'helmet_status': 'No Helmet',
    'number_plate_present': 'No',
    'plate_number': 'MH12AB1234',
    'passenger_count': 3
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
        return redirect('image_analysis')

    return redirect('image_analysis')



# LOGOUT FUNCTION
def Logoutview(request):
    logout(request)
    return redirect('login')
