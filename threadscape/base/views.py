from . import models, forms
from django.db.models import Q
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404


#-Function to render the login page-#
def login_page(request: HttpRequest):

    #-Base object-#
    page = "login"

    #-Redirecting to the homepage if the user is authenticated-#
    if request.user.is_authenticated:
        return redirect("home")

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Getting the user login details-#
        username = request.POST.get("username").lower()
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
    context = {"page": page}

    #-Returning the rendered page-#
    return render(request, "base/login.html", context)


#-Function to logout the user-#
def logout_user(request: HttpRequest):

    #-Logging out the user and redirecting to the home page-#
    logout(request)
    return redirect("home")


#-Function to render the login page but for registration-#
def register_page(request: HttpRequest):

    #-Creating the registration form object from the User model-#
    form = UserCreationForm()

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Filling the form object using the submitted data-#
        form = UserCreationForm(request.POST)

        #-Checking if the form and its data is valid-#
        if form.is_valid():

            #-Getting the user data without saving to the database-#
            user = form.save(commit = False)

            #-Performing some cleanup like lowercasing the username-#
            user.username = user.username.lower()

            #-Saving the cleaned data to the database-#
            user.save()

            #-Logging the user in and redirecting to the home page-#
            login(request, user)
            return redirect("home")

        #-Returning an error flash message if invalid form-#
        else:
            messages.error(request, "An error occurred during registration.")

    #-Creating the context object to render-#
    context = {"form": form}

    #-Returning the rendered page-#
    return render(request, "base/login.html", context)


#-Function to render the homepage-#
def home(request: HttpRequest):

    #-Getting the topic filter if given else using star-#
    topic = request.GET.get("topic", "")

    #-Fetching all the thread and topic records-#
    topics = models.Topic.objects.all()
    threads = models.Thread.objects.filter(
        Q(topic__name__icontains = topic) |
        Q(name__icontains = topic) |
        Q(description__icontains = topic)
    )

    #-Fetching the messages-#
    thread_messages = models.Message.objects.filter(Q(thread__topic__name__icontains = topic))

    #-Creating the context object to render-#
    context = {
        "topics": topics,
        "threads": threads,
        "thread_count": threads.count(),
        "thread_messages": thread_messages,}

    #-Returning the rendered page-#
    return render(request, "base/home.html", context)


#-Function to render the selected thread-#
def thread(request: HttpRequest, pk: str):

    #-Getting the thread using the thread ID-#
    thread = get_object_or_404(models.Thread, id = pk)

    #-Getting the messages for the given thread-#
    thread_messages = models.Message.objects.filter(thread = pk)
    thread_messages = thread.message_set.all()

    #-Getting all the participants of the thread-#
    participants = thread.participants.all()

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Creating a message in the Message model using the POST data-#
        models.Message.objects.create(
            user = request.user,
            thread = thread,
            body = request.POST.get("body")
        )

        #-Adding the user to the participants list-#
        thread.participants.add(request.user)

        #-Returning the user to the same thread page-#
        return redirect("thread", pk = thread.id)

    #-Creating the context object to render-#
    context = {"thread": thread, "thread_messages": thread_messages, "participants": participants}

    #-Returning the rendered page-#
    return render(request, "base/thread.html", context)


#-Function to render the selected user profile-#
def profile(request: HttpRequest, pk: str):

    #-Getting the user data from the id-#
    user = get_object_or_404(models.User, id = pk)

    #-Fetching all the thread and topic records-#
    topics = models.Topic.objects.filter()
    threads = user.thread_set.all()

    #-Fetching the messages-#
    thread_messages = user.message_set.all()

    #-Creating the context object to render-#
    context = {"user": user, "threads": threads, "topics": topics, "thread_count": threads.count(), "thread_messages": thread_messages}

    #-Returning the rendered page-#
    return render(request, "base/profile.html", context)


#-Function to delete a message from a thread-#
@login_required(login_url = "login")
def delete_message(request: HttpRequest, pk: str):

    #-Getting the message for the given id-#
    message = get_object_or_404(models.Message, id = pk)
    thread_id = message.thread.id

    #-Deleting the record and redirecting to home if the request was through form submit-#
    if request.method == "POST":
        message.delete()
        return redirect("home")
        return redirect("thread", pk = thread_id)

    #-Creating the context object to render-#
    context = {"object": message}

    #-Returning the rendered page-#
    return render(request, "base/delete.html", context)


#-Function to render threads with the selected topic-#
def topic(request: HttpRequest, pk: str):

    #-Getting the topic from the id and threads based on the topic id-#
    topic = get_object_or_404(models.Topic, id = pk)
    threads = models.Thread.objects.filter(topic = topic)

    #-Creating the context object to render-#
    context = {"topic": topic, "threads": threads}

    #-Returning the rendered page-#
    return render(request, "base/topic.html", context)


#-Function to render the thread creation page or create thread-#
@login_required(login_url = "login")
def create_thread(request: HttpRequest):

    #-Creating the form and topics object-#
    form = forms.ThreadForm()
    topics = models.Topic.objects.all()

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Getting the topic name-#
        topic_name = request.POST.get("topic")

        #-Getting the topic from the name if exist else creating and fetching it-#
        topic, _ = models.Topic.objects.get_or_create(name = topic_name)

        #-Adding the new form data to the Thread model-#
        models.Thread.objects.create(
            topic = topic,
            host = request.user,
            name = request.POST.get("name"),
            description = request.POST.get("description"),
        )

        #-Redirecting to the homepage-#
        return redirect("home")

    #-Creating the context object to render-#
    context = {"form": form, "topics": topics, "mode": "Create"}

    #-Returning the rendered page-#
    return render(request, "base/thread_form.html", context)


#-Function to update the thread details-#
@login_required(login_url = "login")
def update_thread(request: HttpRequest, pk: str):

    #-Getting the thread from the ID and filling the form with it-#
    thread = get_object_or_404(models.Thread, id = pk)
    form = forms.ThreadForm(instance = thread)

    #-Creating the topics object-#
    topics = models.Topic.objects.all()

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Getting the topic name-#
        topic_name = request.POST.get("topic")

        #-Getting the topic from the name if exist else creating and fetching it-#
        topic, _ = models.Topic.objects.get_or_create(name = topic_name)

        #-Adding the form data to the thread instance-#
        thread.topic = topic
        thread.name = request.POST.get("name")
        thread.description = request.POST.get("description")

        #-Saving the updated data to the thread instance-#
        thread.save()

        #-Redirecting to the homepage-#
        return redirect("home")

    #-Creating the context object to render-#
    context = {"form": form, "topics": topics, "thread": thread, "mode": "Update"}

    #-Returning the rendered page-#
    return render(request, "base/thread_form.html", context)


#-Function to delete the selected thread-#
@login_required(login_url = "login")
def delete_thread(request: HttpRequest, pk: str):

    #-Getting the thread for the given id-#
    thread = get_object_or_404(models.Thread, id = pk)

    #-Deleting the record and redirecting to home if the request was through form submit-#
    if request.method == "POST":
        thread.delete()
        return redirect("home")

    #-Creating the context object to render-#
    context = {"object": thread}

    #-Returning the rendered page-#
    return render(request, "base/delete.html", context)

#-Function to delete the selected thread-#
@login_required(login_url = "login")
def update_profile(request: HttpRequest):

    #-Creating the form from the user instance-#
    form = forms.UserForm(instance = request.user)

    #-Creating a new user-#
    user = models.User.objects.get(id = request.user.id)

    #-Checking if method is POST, meaning form was submitted-#
    if request.method == "POST":

        #-Getting the copy of the POST request-#
        post_data = request.POST.copy()

        #-Lowercasing the username-#
        post_data["username"] = post_data["username"].lower()

        #-Filling the form object using the submitted data-#
        form = forms.UserForm(post_data, instance = user)

        #-Checking if the form and its data is valid-#
        if form.is_valid():

            #-Saving the updated data-#
            form.save()

            #-Redirecting to the home page-#
            return redirect("profile", pk = request.user.id)

        #-Else returning error message-#
        else:

            #-Throwing username taken message if username exists-#
            if form.errors.get("username"):
                messages.error(request, f"The username '{request.POST.get('username')}' is already taken.")

            #-Else throwing a general error response-#
            else:
                messages.error(request, "Please correct the errors below.")

    #-Creating the context object to render-#
    context = {"form": forms.UserForm(instance = request.user)}

    #-Returning the rendered page-#
    return render(request, "base/profile_settings.html", context)
