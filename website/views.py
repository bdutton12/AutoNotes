import tk
from email.mime import message
from re import L
from django.forms import CharField
from django.shortcuts import  render, redirect
from .forms import ImageUploadForm, NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from AutoNotes import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from website.models import Post
from website.models import Person
from text_translator import run_model
from django.urls import reverse_lazy
import numpy as np

# Create your views here.
from django.http import HttpResponse

# Homepage
def index(request):
    username = "anon"
    post_list = []
    # If user is logged in
    if request.user.is_authenticated:
        username = request.user.username

        # Get list of users with corresponding username (should only be one but django insists list)
        user = list(Person.objects.filter(username=username))

        user_obj = None
        if len(user) > 0:
            user_obj = user[0]

        # Append image path and text to post list as tuple
        for post in user_obj.notes.all():
            img = post.image
            post_tup = (post.text, img.url)
            post_list.append(post_tup)

    # Objects to pass to index.html
    context = {
        "welcome_msg": "Hello {}!".format(username),
        "posts": post_list
    }

    # Render index with data
    return render(request, 'index.html', context=context)

def register_request(request):
    # Initialize content for thank you email
    #email_contents = "Thank you for signing up! If you have any questions, feel free to contact me at bdutton12@outlook.com."

    if request.method == "POST":
        form = NewUserForm(request.POST)

        # If information is entered in proper format
        if form.is_valid():
            # Create user object and login user
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            
            # Create user model in db
            user_db = Person(username=request.user.username)
            user_db.save()
            
            # Send thank you email and return to homepage (leaving out for now)
            #send_mail(subject="Thanks for Registering with AutoNotes!", message=email_contents, recipient_list=[user.email], from_email=settings.EMAIL_HOST_USER)
            return redirect("index")

    # If form incorrect or invalid, attempt to register again
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        # If information was entered in proper format
        if form.is_valid():
            # Get username and pass from form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Sign user in and assign to var
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Give success message and redirect to homepage
                messages.success(request, "You are now logged in as {}".format(username))
                return redirect("index")
            else:
                messages.error(request, "The username or password was invalid.")
        else:
            messages.error(request, "The username or password was invalid.")
    
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

# Logout user
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(index)

# Upload image function
def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create form post containing image, then use image to run NN on text
            post = form.save()
            image = post.image.path
            text = run_model.run_model(image)
            print(text)
            post.text = text
            post.save()

            # Add post to list of user posts
            user = list(Person.objects.filter(username=request.user.username))

            if len(user) < 0 or len(user) > 1:
                logout(request, request.user)
                return redirect("login")

            user[0].notes.add(post)
            user[0].save()

        return redirect("index")
	
    form = ImageUploadForm()
    return render(request=request, template_name="upload.html", context={'form':form})
