from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

# Create your views here.
def index(request):
	context={'next':"/"}
	if "next" in request.GET:
		context={'next':request.GET["next"]}
	if request.method=="POST":
		user = authenticate(username=request.POST["username"], password=request.POST["password"])
		if user is None:
			context={'error':True}
		else:
			login(request, user)
			if "next" in request.POST and request.POST["next"]!="":
				return redirect(request.POST["next"])
	
	
	return render(request, 'index.html',context)

@login_required(login_url='/')
def salir(request):
    logout(request)
    return redirect('/')