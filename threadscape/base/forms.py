from django.forms import ModelForm
from . import models

class ThreadForm(ModelForm):
    class Meta:
        model = models.Thread
        fields = ["name", "description", "topic"]
        fields = "__all__"
