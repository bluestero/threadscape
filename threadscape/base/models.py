from django.db import models
from django.contrib.auth.models import User


#-Model class for Topic table-#
class Topic(models.Model):

    #-Columns and their attributes for the table-#
    name = models.CharField(max_length = 200)

    #-Function to return the string represenation of the class object-#
    def __str__(self):
        return self.name


#-Model class for Thread table-#
class Thread(models.Model):

    #-Columns and their attributes for the table-#
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length = 128)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name = "participants", blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    #-Function to return the string represenation of the class object-#
    def __str__(self):
        return self.name

    #-Meta class to define the metadata of the table-#
    class Meta:

        #-Changing the order of the records displayed-#
        ordering = ["-updated", "-created"]


#-Model class for Message table-#
class Message(models.Model):

    #-Columns and their attributes for the table-#
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    #-Meta class to define the metadata of the table-#
    class Meta:

        #-Changing the order of the records displayed-#
        ordering = ["-updated", "-created"]

    #-Function to return the string represenation of the class object-#
    def __str__(self):
        return self.body[:50]
