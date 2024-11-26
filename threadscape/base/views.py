from django.shortcuts import render
from . import models, forms


# Create your views here.
def home(request):
    threads = models.Thread.objects.all()
    context = {"threads": threads}
    return render(request, "base/home.html", context)

def thread(request, pk):
    thread = models.Thread.objects.get(id = pk)
    context = {"thread": thread}
    return render(request, "base/thread.html", context)

def create_thread(request):
    form = forms.ThreadForm()
    context = {"form": form}
    return render(request, "base/thread_form.html", context)
