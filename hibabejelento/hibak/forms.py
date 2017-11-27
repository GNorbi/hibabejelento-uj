from django.forms import ModelForm
from .models import Hiba
from django.forms import TextInput

class HibaBejelentoForm(ModelForm):
	class Meta:
		model = Hiba
		fields = ('nev', 'cim','kapcsolattarto_email', 'leiras')
        #fields = ('nev', 'cim','kapcsolattarto_email')
        #nev = forms.CharField()
        #email = forms.EmailField()
        #telefonszam = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Telefonszamot a kovetkezo formatumban kell megadni: '+999999999'."))
        #cim = forms.CharField()

		