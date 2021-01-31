from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from app1.models import Account
# Create your views here.

def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.info(request,"Invalid credentials!")
            return redirect('login')


    else:
        return render(request, 'login.html')



def logout(request):
	auth.logout(request)
	return redirect('home')

def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1==password2:
        	
        	if Account.objects.filter(email=email).exists() or Account.objects.filter(username=username).exists()  :
        		messages.info(request,"Email or username taken!")
        		return redirect('register')
        	else:	
                #Account.objects.filter(email=email).update(status=status)
		        user=Account.objects.create_user(email=email,password=password1,username=username)
		        user.save()
                
		        return render(request, 'register2.html',{'email':email})
        else:
        	messages.info(request,"Password not matching!")
        	return redirect('register')
       	messages.info(request,"Now you are registered!, YOU CAN LOGIN")
        return redirect('register')

    else:
    	return render(request, 'register.html')

def register2(request):
    if request.method == 'POST':
        status=request.POST['status']
        email=request.POST['email']
        Account.objects.filter(email=email).update(status=status)
        return redirect('login')
        

    else:
        return render(request, 'register2.html')