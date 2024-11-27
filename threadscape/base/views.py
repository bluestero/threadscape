from . import models, forms
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


#-Function to render the login page-#
def login_page(request):

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Getting the user login details-#
        username = request.POST.get("username")
        password = request.POST.get("password")

        #-Getting the record with the username from the User model-#
        user = models.User.objects.filter(username = username)

        #-Checkig if the user exists in our database-#
        if user.exists():

            #-Getting the user authenticated-#
            user = authenticate(request, username = username, password = password)

            #-Logging in the user and redirecting to the home directory if authentication is successful-#
            if user:
                login(request, user)
                return redirect("home")


            #-Throwing error if the authentication failed-#
            else:
                messages.error(request, f"Invalid password entered for '{username}'.")

        #-Throwing error message if a user does not exist-#
        else:
            messages.error(request, f"User '{username}' does not exist.")

    #-Creating the context object to render-#
    context = {}

    #-Returning the rendered page-#
    return render(request, "base/login.html", context)


#-Function to logout the user-#
def logout_user(request):

    #-Logging out the user and redirecting to the home page-#
    logout(request)
    return redirect("home")


#-Function to render the homepage-#
def home(request):

    #-Getting the topic filter if given else using star-#
    topic = request.GET.get("topic", "")

    #-Fetching all the thread and topic records-#
    topics = models.Topic.objects.all()
    threads = models.Thread.objects.filter(
        Q(topic__name__icontains = topic) |
        Q(name__icontains = topic) |
        Q(description__icontains = topic)
    )

    #-Creating the context object to render-#
    context = {"threads": threads, "topics": topics, "room_count": threads.count()}

    #-Returning the rendered page-#
    return render(request, "base/home.html", context)


#-Function to render the selected thread-#
def thread(request, pk):

    #-Getting the thread using the thread ID-#
    thread = models.Thread.objects.get(id = pk)

    #-Creating the context object to render-#
    context = {"thread": thread}

    #-Returning the rendered page-#
    return render(request, "base/thread.html", context)


#-Function to render threads with the selected topic-#
def topic(request, pk):

    #-Getting the topic from the id and threads based on the topic id-#
    topic = models.Topic.objects.get(id = pk)
    threads = models.Thread.objects.filter(topic = topic)

    #-Creating the context object to render-#
    context = {"topic": topic, "threads": threads}

    #-Returning the rendered page-#
    return render(request, "base/topic.html", context)


#-Function to render the thread creation page or create thread-#
@login_required(login_url = "login-page")
def create_thread(request):

    #-Creating the form object-#
    form = forms.ThreadForm()

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Filling the form object using the submitted data-#
        form = forms.ThreadForm(request.POST)

        #-Saving the data to the model if valid and redirecting to the homepage-#
        if form.is_valid():
            form.save()
            return redirect("home")

    #-Creating the context object to render-#
    context = {"form": form}

    #-Returning the rendered page-#
    return render(request, "base/thread_form.html", context)


#-Function to update the thread details-#
@login_required(login_url = "login-page")
def update_thread(request, pk):

    #-Getting the thread from the ID and filling the form with it-#
    thread = models.Thread.objects.get(id = pk)
    form = forms.ThreadForm(instance = thread)

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Filling the form object using the submitted data and linking to the thread instance-#
        form = forms.ThreadForm(request.POST, instance = thread)

        #-Saving the data to the model if valid and redirecting to the homepage-#
        if form.is_valid():
            form.save()
            return redirect("home")

    #-Creating the context object to render-#
    context = {"form": form}

    #-Returning the rendered page-#
    return render(request, "base/thread_form.html", context)


#-Function to delete the selected thread-#
@login_required(login_url = "login-page")
def delete_thread(request, pk):

    #-Getting the thread for the given id-#
    thread = models.Thread.objects.filter(id = pk)

    #-Deleting the record and redirecting to home if the request was through form submit-#
    if request.method == "POST" and thread.exists():
        thread.delete()
        return redirect("home")

    #-Creating the context object to render-#
    context = {"object": thread}

    #-Returning the rendered page-#
    return render(request, "base/delete.html", context)
