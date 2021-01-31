from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import logging, traceback
from app1.forms import *
from app1.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

        
# Create your views here.




def home(request):
	
	return render(request,"home.html",)


def students(request):
	allusers=Account.objects.all().exclude(role="mentor")
	
	return render(request,"students.html",{'allusers':allusers})

def courses(request):
	if request.method == 'POST':
		code=request.POST['code']
		Items.objects.all().filter(code=code).delete()
		courses=Items.objects.all()
		return render(request,"courses.html",{'courses':courses})
	courses=Items.objects.all()
	return render(request,"courses.html",{'courses':courses})



def detailcourse(request,value):
	course=Items.objects.get(code=value)
	courses=Items.objects.all()
	stu = {"course":course,"courses":courses}
	return render(request,"courses2.html",stu)


def editcourse(request,value):
	course=Items.objects.get(code=value)
	courses = Items.objects.all()
	stu = {"course": course,"courses":courses
	}
	queryset = Items.objects.get(code=value)
	form=itemforms(instance=queryset)
	if request.method == 'POST':
		form = itemforms(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.info(request,"Update success!")
			course=Items.objects.get(code=value)
			courses = Items.objects.all()
			stu = {"course": course,"courses":courses
			}
			return render(request,"editcourse.html",stu)	
		else:
			course=Items.objects.get(code=value)
			courses = Items.objects.all()
			stu = {"course": course,"courses":courses
			}
			messages.info(request,"This name already exists!")
			return render(request,"editcourse.html",stu)	
	course=Items.objects.get(code=value)
	courses = Items.objects.all()
	stu = {"course": course,"courses":courses
	}
	return render(request,"editcourse.html", stu)	


def addcourse(request):
	if request.method=='POST':
		name=request.POST['name']
		code=request.POST['code']
		program=request.POST['program']
		points=request.POST['points']
		sem_redovni=request.POST['sem_redovni']
		sem_izvanredni=request.POST['sem_izvanredni']
		izborni=request.POST['izborni']
		if Items.objects.filter(code=code).exists():
			messages.info(request,"This code is taken!")
			return render(request,"addcourse.html")
		if Items.objects.filter(name=name).exists() :
			messages.info(request,"This name is taken!")
			return render(request,"addcourse.html")
		else: 
			model=Items(name=name,code=code,program=program,points=points,sem_redovni=sem_redovni,sem_izvanredni=sem_izvanredni,izborni=izborni)
			model.save()
			messages.info(request,"Course is saved!")
			return render(request,"addcourse.html")

	return render(request,"addcourse.html")


def editstatus(request,value,vale):
	if request.method == 'POST':
		status=request.POST['status']
		Enrollment.objects.all().filter(user_id_id=value,itemid_id=vale).update(status=status)
		enroll=Enrollment.objects.all().filter(user_id_id=value,itemid_id=vale)
		enroll2=Enrollment.objects.all().filter(user_id_id=value)
		items=Items.objects.all()
		account=Account.objects.filter(id=value)
		stu = {"enroll": enroll,"items":items,"enroll2":enroll2,"account":account,
		}
		messages.info(request,"Update success!")
		return render(request,"studliststatus.html", stu)			
	account=Account.objects.filter(id=value)
	enroll=Enrollment.objects.all().filter(user_id_id=value,itemid_id=vale)
	enroll2=Enrollment.objects.all().filter(user_id_id=value)
	items=Items.objects.all()
	stu = {"enroll":enroll,"items":items,"enroll2":enroll2,"account":account,}	
	return render(request,"studliststatus.html",stu)



def list(request,value,vale):
	if request.method == 'POST':
		if vale==0:
			code=request.POST['code']
			Enrollment.objects.all().filter(user_id_id=value,itemid_id=code).delete()
			if Account.objects.filter(id=value,status="redovni"):
				items=Items.objects.all().order_by('sem_redovni')
				account=Account.objects.filter(id=value)
				enroll=Enrollment.objects.all().filter(user_id_id=value)
				my=enroll.values_list('itemid_id',flat=True)
				fill=Items.objects.all().exclude(code__in=my)
				messages.info(request,"Delete success!")
				stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'redovni'}	
				return render(request,"list.html",stu)
			else:
				items=Items.objects.all().order_by('sem_izvanredni')
				account=Account.objects.filter(id=value)
				enroll=Enrollment.objects.all().filter(user_id_id=value)
				my=enroll.values_list('itemid_id',flat=True)
				messages.info(request,"Delete success!")
				fill=Items.objects.all().exclude(code__in=my)
				stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'izvanredni'}	
				return render(request,"list.html",stu)


		
		if vale==1:
			code=request.POST['code']
			enro=Enrollment(user_id_id=value,itemid_id=code,status="nepoloženo")
			enro.save()
			if Account.objects.filter(id=value,status="redovni"):
				items=Items.objects.all().order_by('sem_redovni')
				account=Account.objects.filter(id=value)
				enroll=Enrollment.objects.all().filter(user_id_id=value)
				my=enroll.values_list('itemid_id',flat=True)
				fill=Items.objects.all().exclude(code__in=my)
				messages.info(request,"Update success!")
				stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'redovni'}	
				return render(request,"list.html",stu)
			else:
				items=Items.objects.all().order_by('sem_izvanredni')
				account=Account.objects.filter(id=value)
				enroll=Enrollment.objects.all().filter(user_id_id=value)
				my=enroll.values_list('itemid_id',flat=True)
				fill=Items.objects.all().exclude(code__in=my)
				messages.info(request,"Update success!")
				stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'izvanredni'}	
				return render(request,"list.html",stu)
		if vale==3:
			code=request.POST['code']
			status=request.POST['status']
			Enrollment(user_id_id=value,itemid_id=code,status="status")
			
			if Account.objects.filter(id=value,status="redovni"):
				items=Items.objects.all().order_by('sem_redovni')
				account=Account.objects.filter(id=value)
				enroll=Enrollment.objects.all().filter(user_id_id=value)
				my=enroll.values_list('itemid_id',flat=True)
				fill=Items.objects.all().exclude(code__in=my)
				messages.info(request,"Update success!")
				stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'redovni'}	
				return render(request,"list.html",stu)
			else:
				items=Items.objects.all().order_by('sem_izvanredni')
				account=Account.objects.filter(id=value)
				enroll=Enrollment.objects.all().filter(user_id_id=value)
				my=enroll.values_list('itemid_id',flat=True)
				fill=Items.objects.all().exclude(code__in=my)
				messages.info(request,"Update success!")
				stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'izvanredni'}	
				return render(request,"list.html",stu)
	
	if Account.objects.filter(id=value,status="redovni"):
		items=Items.objects.all().order_by('sem_redovni')
		account=Account.objects.filter(id=value)
		enroll=Enrollment.objects.all().filter(user_id_id=value)
		my=enroll.values_list('itemid_id',flat=True)
		fill=Items.objects.all().exclude(code__in=my)
		stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'redovni'}	
		return render(request,"list.html",stu)
		
	else:
		items=Items.objects.all().order_by('sem_izvanredni')
		account=Account.objects.filter(id=value)
		enroll=Enrollment.objects.all().filter(user_id_id=value)
		my=enroll.values_list('itemid_id',flat=True)
		fill=Items.objects.all().exclude(code__in=my)
		stu = {"enroll":enroll,"items":items,"account":account,"fill":fill,"id":value,"izvorvan":'izvanredni'}	
		return render(request,"list.html",stu)

'''field_name = 'name'
obj = MyModel.objects.first()
field_object = MyModel._meta.get_field(field_name)
field_value = getattr(obj, field_object.attname)'''

