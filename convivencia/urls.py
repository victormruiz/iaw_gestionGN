from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^historial/(?P<alum_id>[0-9]+)/(?P<prof>[a-z]*)$', views.historial),
	url(r'^(?P<tipo>[a-z]+)/(?P<alum_id>[0-9]+)$', views.parte),
	url(r'^resumen/(?P<tipo>[a-z]+)$', views.resumen_hoy),
	url(r'^resumen/(?P<tipo>[a-z]+)/(?P<mes>[0-9]+)/(?P<ano>[0-9]+)$', views.resumen),
	url(r'^show/(?P<tipo>[a-z]+)/(?P<mes>[0-9]+)/(?P<ano>[0-9]+)/(?P<dia>[0-9]+)$', views.show),
	
]
