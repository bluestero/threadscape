from django.shortcuts import render, redirect
from . import models, forms


# Create your views here.
def home(request):
    threads = models.Thread.objects.all()
    topics = models.Topic.objects.all()
    context = {"threads": threads, "topics": topics}
    return render(request, "base/home.html", context)


def thread(request, pk):
    thread = models.Thread.objects.get(id = pk)
    context = {"thread": thread}
    return render(request, "base/thread.html", context)


def topic(request, pk):
    topic = models.Topic.objects.get(id = pk)
    threads = models.Thread.objects.filter(topic = topic)
    print(threads)
    context = {"topic": topic, "threads": threads}
    return render(request, "base/topic.html", context)


def create_thread(request):

    form = forms.ThreadForm()

    if request.method == "POST":
        form = forms.ThreadForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("home")

    context = {"form": form}
    return render(request, "base/thread_form.html", context)


def update_thread(request, pk):

    thread = models.Thread.objects.get(id = pk)
    form = forms.ThreadForm(instance = thread)

    if request.method == "POST":

        form = forms.ThreadForm(request.POST, instance = thread)

        if form.is_valid():
            form.save()

            return redirect("home")

    context = {"form": form}

    return render(request, "base/thread_form.html", context)


def delete_thread(request, pk):

    thread = models.Thread.objects.filter(id = pk)

    if request.method == "POST" and thread.exists():

        thread.delete()

        return redirect("home")

    context = {"object": thread}

    return render(request, "base/delete.html", context)
