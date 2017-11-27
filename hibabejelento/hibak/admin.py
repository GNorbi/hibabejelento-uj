from django.contrib import admin
from .models import Hiba, Visszajelzes, AllapotValtozas
from django.core.mail import send_mail
from django.forms import ModelForm
admin.site.register(Hiba)
admin.site.register(Visszajelzes)

