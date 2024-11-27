from django.apps import AppConfig


#-BaseConfig class fo rthe base app-#
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
