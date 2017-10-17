from django import forms
from django.forms import ModelForm,ModelChoiceField
from convivencia.models import Amonestaciones,Sanciones
from centro.models import Profesores
from django.forms.widgets import CheckboxSelectMultiple,HiddenInput,DateInput,Textarea,TextInput,Select,SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget 
from datetime import date



class AmonestacionForm(forms.ModelForm):
	Profesor = ModelChoiceField(Profesores.objects.all().order_by("Apellidos"), empty_label=None)
	class Meta:
		model = Amonestaciones
		fields = "__all__"
		widgets = {
			'IdAlumno':HiddenInput(),
			'Fecha':SelectDateWidget(),
                        'Comentario': Textarea(attrs={'cols': 80, 'rows': 15}),
			
			#'Comentario': TinyMCE(),

        }

class SancionForm(forms.ModelForm):
	class Meta:
		model = Sanciones
		fields = "__all__"
		widgets = {
			'IdAlumno':HiddenInput(),
			'Fecha':SelectDateWidget(),
			'Fecha_fin':SelectDateWidget(),
			
			'Sancion':TextInput(attrs={'size': '67'}),
			'Comentario': Textarea(attrs={'cols': 80, 'rows': 15}),
			#'Comentario': TinyMCE(),
            
        }


class FechasForm(forms.Form):
	try:
		Fecha1	= forms.DateField(initial=Amonestaciones.objects.first().Fecha,widget=forms.SelectDateWidget(years=range(2000, 2100)))
	except:
		Fecha1	= forms.DateField(initial=date.today,widget=forms.SelectDateWidget(years=range(2000, 2100)))
	Fecha2	= forms.DateField(initial=date.today,widget=forms.SelectDateWidget(years=range(2000, 2100)))
	