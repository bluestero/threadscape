from django.forms import ModelForm
from . import models


#-ModelForm class for Thread-#
class ThreadForm(ModelForm):

    #-Meta class to define the model and fields to show-#
    class Meta:
        fields = "__all__"
        model = models.Thread
        exclude = ["host", "participants"]
