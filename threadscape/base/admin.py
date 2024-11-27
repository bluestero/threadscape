from django.contrib import admin
from . import models

#-Registering the database models-#
admin.site.register(models.Thread)
admin.site.register(models.Topic)
admin.site.register(models.Message)
