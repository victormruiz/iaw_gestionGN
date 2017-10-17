from django import forms
from centro.models import Cursos,Departamentos,Areas

class UnidadForm(forms.Form):
	Unidad = forms.ModelChoiceField(queryset=Cursos.objects.order_by('Curso'), empty_label=None,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))

class DepartamentosForm(forms.Form):
        Areas = forms.ModelChoiceField(queryset=Areas.objects.all(),required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))
        Departamento = forms.ModelChoiceField(queryset=Departamentos.objects.order_by('Nombre'), required=False,widget=forms.Select(attrs={'class': "form-control",'onchange': 'this.form.submit();'}))

        def __init__(self, *args, **kwargs):
            super(DepartamentosForm, self).__init__(*args, **kwargs)
            if args[0].has_key("Areas") and args[0]["Areas"]!="":
                areas=Areas.objects.get(id=args[0]["Areas"])
                self.fields['Departamento']. queryset= areas.Departamentos.all()
                self.fields['Departamento'].initial=args[0]["Departamento"]
