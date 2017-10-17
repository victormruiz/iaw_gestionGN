from django.contrib import admin
from convivencia.models import Amonestaciones,Sanciones,TiposAmonestaciones
# Register your models here.


class AmonestacionesAdmin(admin.ModelAdmin):
    #date_hierarchy = 'Fecha_nacimiento'
    actions_selection_counter=False
    list_filter = ['Fecha','Profesor']
    list_display = ["Fecha","IdAlumno","Comentario"]
     
    search_fields = ['Comentario']

class SancionesAdmin(admin.ModelAdmin):
    #date_hierarchy = 'Fecha_nacimiento'
    actions_selection_counter=False
    list_filter = ['Fecha']
    list_display = ["Fecha","Fecha_fin","IdAlumno","Sancion"]
     
    search_fields = ['Comentario']

admin.site.register(TiposAmonestaciones)
admin.site.register(Amonestaciones,AmonestacionesAdmin)
admin.site.register(Sanciones,SancionesAdmin)

