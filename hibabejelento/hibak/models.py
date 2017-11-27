from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.core.mail import send_mail
from datetime import datetime

class Hiba(models.Model):
	id = models.AutoField(primary_key=True)
	nev = models.CharField(max_length=200,help_text="Adja meg a hiba bejelentő nevét", default='')
	cim = models.CharField(max_length=200,help_text="Adja meg a hiba címét", default='')
	kapcsolattarto_email = models.EmailField(max_length=254, help_text="Ezen az emailen lesz tájékoztatva a hibajavításról")
	leiras = models.TextField(max_length=2000)
	bejelentes_datuma=models.DateTimeField(default=datetime.utcnow, blank=True)

	hiba_allapot = (
		('f', 'Fogadva'),
		('g', "Hibajavítás folyamatba helyezve"),
		('h', "Hibajavítás azonnal nem lehetséges, ajánlatkészítés folyamatban"),
		('i', "Hibajavítás azonnal nem lehetséges, alkatrészre vár"),
		('j', "A hiba javítása elkészült"),
    	)
	statusz = models.CharField(max_length=1, choices=hiba_allapot, blank=True, default='f', help_text='Hiba Allapot')
	allapotvaltozasok_szama = models.PositiveSmallIntegerField(default=0)
	
	class Meta:
        	verbose_name = 'Hibák'
        	verbose_name_plural = 'Hibák'	
	
	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return str(self.id).encode('UTF-8') + " - " + (self.nev).encode('UTF-8') + " - " + (self.cim).encode('UTF-8') 

	def __init__(self, *args, **kwargs):
		super(Hiba, self).__init__(*args, **kwargs)
		self.__original_statusz = self.statusz

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		elso = " sorszámu hiba"
		masodik = "A "
		harmadik = " sorszámon bejelentett hiba állapota  megváltozott, megtekintheti  www.kincstarhibabejelento.hu webcímen üzemelő hibabejelentő felületen. Ez egy automatikus üzenet, kérjük erre ne válaszoljon.  Tisztelettel: Ép-Üz-Bau Kft"
		sorszamu = " sorszámú hiba állapota megváltozott"
		
		if self.statusz != self.__original_statusz:
			send_mail(str(self.id).decode('utf-8') + elso.decode('utf-8'),masodik.decode('utf-8') + str(self.id).decode('utf-8') + harmadik.decode('utf-8'), str(self.id).decode('utf-8') + " " + sorszamu.decode('utf-8') + ' <tesztemailepuzbau@gmail.com>',[self.kapcsolattarto_email],fail_silently=False,)
			AllapotValtozas.objects.create(hiba=self, uj_statusz = self.statusz) #allapotvaltozas objektum elkeszitese
		super(Hiba, self).save(force_insert, force_update, *args, **kwargs)
		self.__original_statusz = self.statusz

	def get_absolute_url(self):
		"""
		Returns the url to access a particular book instance.
		"""
		return reverse('hibareszletei', args=[str(self.id)])


class AllapotValtozas(models.Model):
	hiba = models.ForeignKey('Hiba', on_delete=models.SET_NULL, null=True)
	hiba_allapot = (
		('f', 'Fogadva'),
		('g', "Hibajavítás folyamatba helyezve"),
		('h', "Hibajavítás azonnal nem lehetséges, ajánlatkészítés folyamatban"),
		('i', "Hibajavítás azonnal nem lehetséges, alkatrészre vár"),
		('j', "A hiba javítása elkészült"),
    )
	uj_statusz = models.CharField(max_length=1, choices=hiba_allapot, blank=True, default='f', help_text='Hiba Allapot')
	valtozas_datuma=models.DateTimeField(default=datetime.utcnow, blank=True)
	
	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		self.hiba.allapotvaltozasok_szama = self.hiba.allapotvaltozasok_szama + 1
		super(AllapotValtozas, self).save(force_insert, force_update, *args, **kwargs)



class Visszajelzes(models.Model):
    hiba = models.ForeignKey('Hiba', on_delete=models.SET_NULL, null=True)
    uzenet = models.TextField(max_length=2000)
    datum=models.DateTimeField(default=datetime.utcnow, blank=True)

    class Meta:
        verbose_name = 'Visszajelzések'
        verbose_name_plural = 'Visszajelzések'

    def __str__(self):
        if self.hiba:
            return str(self.hiba.id).encode('UTF-8') + " -- " + (self.uzenet).encode('UTF-8')
        else:
            return (self.uzenet).encode('UTF-8')

    def save(self):
        elso = "sorszámu hiba"
        masodik = "A "
        harmadik = " sorszámon bejelentett hibára visszajelzés érkezett, megtekintheti  www.kincstarhibabejelento.hu webcímen üzemelő hibabejelentő felületen. Ez egy automatikus üzenet, kérjük erre ne válaszoljon.  Tisztelettel: Ép-Üz-Bau Kft"
        sorszamu = "sorszámú hibabejelentésére visszajelzés érkezett"
        send_mail(str(self.hiba.id).decode('utf-8') + " " + elso.decode('utf-8'),masodik.decode('utf-8') + str(self.hiba.id).decode('utf-8') + harmadik.decode('utf-8'), str(self.hiba.id).decode('utf-8') + " " + sorszamu.decode('utf-8') + ' <tesztemailepuzbau@gmail.com>',[self.hiba.kapcsolattarto_email],fail_silently=False,)
        super(Visszajelzes, self).save() # Call the "real" save() method    