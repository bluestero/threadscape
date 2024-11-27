from django.shortcuts import render, redirect
from . import models, forms


#-Function to render the homepage-#
def home(request):

    #-Getting the topic filter if given else using star-#
    topic = request.GET.get("topic", "")

    #-Fetching all the thread and topic records-#
    threads = models.Thread.objects.filter(topic__name__icontains = topic)
    topics = models.Topic.objects.all()

    #-Creating the context object to render-#
    context = {"threads": threads, "topics": topics}

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
