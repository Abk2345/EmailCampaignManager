from django.contrib import admin

# Register your models here.

from .models import Campaign, Subscriber

admin.site.register(Subscriber)
admin.site.register(Campaign)
