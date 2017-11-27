from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^hibabejelentes/$', views.hiba_bejelentes, name='hibabejelentes'),
	url(r'^hibalista/$', views.HibaListaView.as_view(), name='hibalista'),
	url(r'^hibalista/export/$', views.export_hibak_csv, name='export_hibak_csv'),
	url(r'^hibalista/fogadott/$', views.get_fogadott, name='fogadott'),
	url(r'^hibalista/folyamatban/$', views.get_folyamatba_helyezve, name='folyamatban'),
	url(r'^hibalista/elkeszult/$', views.get_elkeszult, name='elkeszult'),
	url(r'^(?P<pk>\d+)$', views.HibaReszleteiView.as_view(), name='hibareszletei'),
]
