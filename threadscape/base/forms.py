from . import models
from django.forms import ModelForm
from django.contrib.auth.models import User


#-ModelForm class for Thread-#
class ThreadForm(ModelForm):

    #-Meta class to define the model and fields to show-#
    class Meta:
        fields = "__all__"
        model = models.Thread
        exclude = ["host", "participants"]


#-ModelForm class for User-#
class UserForm(ModelForm):

    #-Meta class to define the model and fields to show-#
    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name", "email"]
