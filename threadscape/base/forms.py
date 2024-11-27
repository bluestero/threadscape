from django.forms import ModelForm
from . import models


#-ModelForm class for Thread-#
class ThreadForm(ModelForm):

    #-Meta class to define the model and fields to show-#
    class Meta:
        model = models.Thread
        fields = ["name", "description", "topic"]
        fields = "__all__"
