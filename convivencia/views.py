	
# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from convivencia.forms import AmonestacionForm,SancionForm,FechasForm
from centro.models import Alumnos,Profesores
from centro.views import group_check_je
from convivencia.models import Amonestaciones,Sanciones,TiposAmonestaciones
from centro.models import Cursos
from django.contrib.auth.decorators import login_required,user_passes_test
import time,calendar
from datetime import datetime
from operator import itemgetter
from django.db.models import Count
from django.template.loader import get_template
from django.shortcuts import render
from django.template import Context
from django.core.mail import send_mail

# Create your views here.

@login_required(login_url='/')
@user_passes_test(group_check_je,login_url='/')
def parte(request,tipo,alum_id):
	alum=Alumnos.objects.get(pk=alum_id)
	if request.method=='POST':
		if tipo=="amonestacion":
			form = AmonestacionForm(request.POST)
			titulo="Amonestaciones"
		elif tipo=="sancion":
			form = SancionForm(request.POST)
			titulo="Sanciones"
		else:
			return redirect("/")
		
		if form.is_valid():
			form.save()
			return redirect('/centro/alumnos')
	else:
		if tipo=="amonestacion":
			form = AmonestacionForm({'IdAlumno':alum.id,'Fecha':time.strftime("%d/%m/%Y"),'Hora':1,'Profesor':1})
			
			titulo="Amonestaciones"
		elif tipo=="sancion":
			form = SancionForm({'IdAlumno':alum.id,'Fecha':time.strftime("%d/%m/%Y"),'Fecha_fin':time.strftime("%d/%m/%Y"),'Profesor':1})
			titulo="Sanciones"
		else:
			return redirect("/")
		error=False
	context={'alum':alum,'form':form,'titulo':titulo,'tipo':tipo,'menu_alumnos':True}
	return render(request, 'parte.html',context)



@login_required(login_url='/')
@user_passes_test(group_check_je,login_url='/')
def historial(request,alum_id,prof):
	horas=["1ª hora","2ª hora","3ª hora","Recreo","4ª hora","5ª hora","6ª hora"]
	alum=Alumnos.objects.get(pk=alum_id)
	amon=Amonestaciones.objects.filter(IdAlumno_id=alum_id).order_by('Fecha')
	sanc=Sanciones.objects.filter(IdAlumno_id=alum_id).order_by("Fecha")
	
	historial=list(amon)+list(sanc)
	historial=sorted(historial, key=lambda x: x.Fecha, reverse=False)
	
	tipo=[]
	for h in historial:
		if str(type(h)).split(".")[2][0]=="A":
			tipo.append("Amonestación")
		else:
			tipo.append("Sanción")
	hist=zip(historial,tipo,range(1,len(historial)+1))
	prof=True if prof=="" else False
	context={'prof':prof,'alum':alum,'historial':hist,'menu_historial':True,'horas':horas}
	return render(request, 'historial.html',context)


@login_required(login_url='/')
@user_passes_test(group_check_je,login_url='/')
def resumen_hoy(request,tipo):
	hoy=datetime.now()
	return resumen(request,tipo,str(hoy.month),str(hoy.year))


@login_required(login_url='/')
@user_passes_test(group_check_je,login_url='/')
def resumen(request,tipo,mes,ano):
	if request.method=='POST':
		tipo=request.POST.get('tipo')

	c = calendar.HTMLCalendar(calendar.MONDAY)
	calhtml=c.formatmonth(int(ano),int(mes))

	if tipo=="amonestacion":
		datos=Amonestaciones.objects.filter(Fecha__year=ano).filter(Fecha__month=mes)
		titulo="Resumen de amonestaciones"
	if tipo=="sancion":
		datos=Sanciones.objects.filter(Fecha__year=ano).filter(Fecha__month=mes)
		titulo="Resumen de sanciones"
	
	ult_dia=calendar.monthrange(int(ano),int(mes))[1]
	dic_fechas=datos.values("Fecha")
	fechas=[]
	for f in dic_fechas:
		fechas.append(f["Fecha"])

	for dia in range(1,int(ult_dia)+1):
		fecha=datetime(int(ano),int(mes),dia)
		if fecha.date() in fechas:
			calhtml=calhtml.replace(">"+str(dia)+"<",'><a href="/convivencia/show/%s/%s/%s/%s"><strong>%s</strong></a><'%(tipo,mes,ano,dia,dia))
	calhtml=calhtml.replace('class="month"','class="table-condensed table-bordered table-striped"')
	#form=TipoResumen(initial={'tipo':tipo})
	
	
	mes_actual=datetime(int(ano),int(mes),1)
	mes_ant=AddMonths(mes_actual,-1)
	mes_prox=AddMonths(mes_actual,1)

	context={'calhtml':calhtml,'fechas':[mes_actual,mes_ant,mes_prox],'titulo':titulo,'tipo':tipo,'menu_resumen':True}
	return render(request, 'resumen.html',context)

def AddMonths(d,x):
    newmonth = ((( d.month - 1) + x ) % 12 ) + 1
    newyear  = d.year + ((( d.month - 1) + x ) / 12 ) 
    return datetime( int(newyear), newmonth, d.day)

@login_required(login_url='/')
@user_passes_test(group_check_je,login_url='/')
def show(request,tipo,mes,ano,dia):
	fecha=datetime(int(ano),int(mes),int(dia))
	if tipo=="amonestacion":
		datos=Amonestaciones.objects.filter(Fecha=fecha)
		titulo="Resumen de amonestaciones"
	if tipo=="sancion":
		datos=Sanciones.objects.filter(Fecha=fecha)
		titulo="Resumen de sanciones"
	
	datos=zip(range(1,len(datos)+1),datos,ContarFaltas(datos.values("IdAlumno")))
	context={'datos':datos,'tipo':tipo,'fecha':fecha,'titulo':titulo,'menu_'+tipo:True}
	context[tipo]=True
	return render(request, 'show.html',context)


	

def ContarFaltas(lista_id):
	contar=[]
	for alum in lista_id:

		am=str(len(Amonestaciones.objects.filter(IdAlumno_id=alum.values()[0])))
		sa=str(len(Sanciones.objects.filter(IdAlumno_id=alum.values()[0])))

		contar.append(am+"/"+sa)
	return contar
