from django.shortcuts import render,redirect
from django.template import loader
from django import forms
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
import datetime
from django.utils import timezone

#Registration
def register(request):
	if(request.method=="POST"):
		form=RegistrationForm(request.POST)
		if(form.is_valid()):
			form.save()
			return HttpResponseRedirect('/')  #Back To Login Form
	else:
		form=RegistrationForm()
	return render(request,'quizportal/register.html',{'form':form})


#Questions rendering
@login_required(login_url='login')
def detail(request, id_no):

	#Check if logged in user is Admin
	if(request.user.username=='admin'):
		return HttpResponseRedirect('/adminmain')

	else:
		
		#Quiz Ended
		time=Time.objects.all()
		print(time)
		for i in time:
			endtime=i.end_time
			break

		#Time Conversion according to 24hrs clock
		f=(endtime)
		f=str(f).split(" ")
		time=f[1]
		time=str(time).split(":")
		h=str(((int)(time[0])))
		m=str(((int)(time[1])))

		#print(h+":"+m+":"+time[2].split("+")[0])
		
		if(endtime < timezone.now()):
			return HttpResponseRedirect('/ended')


		#Quiz Live
		else:
		
			#POST request
			if(request.method=='POST'):
				id1=(int)(id_no)
				id1=id1-1
				question=QuestionData.objects.filter(id_no=str(id_no))
				question1=QuestionData.objects.filter(id_no=str(id1))
				p1=SolvedQ.objects.filter(Q(q_id=question1.get(id_no=id1)) ,Q(id_no=request.user), Q(check=False))
			

				#Choices
				for i in question1:
					correct_choice1=i.correct_choice
					if(len(p1)==0 and correct_choice1==request.POST.get('choice')):
						obj,notif=SolvedQ.objects.get_or_create(id_no=request.user, q_id=question1.get(id_no=id1), check=True)
						if notif is True:
							obj.save()
					
					else:
						if(len(p1)==0 and correct_choice1!=request.POST.get('choice')):
							obj,notif=SolvedQ.objects.get_or_create(id_no=request.user, q_id=question1.get(id_no=id1), check=False)
							if notif is True:
								obj.save()

				if(len(question)>0):
					args={'question':question, 'timer':h+":"+m+":"+time[2].split("+")[0]}
					return render(request, 'quizportal/questions.html', args)

				else:
					return HttpResponseRedirect('/ended')
		

			#GET request
			else:
				question=QuestionData.objects.all()

				if(len(question)==0):
					return render(request, 'quizportal/noquestions.html')

				else:
					
					id1=(int)(id_no)
					question1=QuestionData.objects.filter(id_no=str(id1))

					#Final Page Reached
					if(len(question1)==0):
						return HttpResponseRedirect('/ended')

					else:

						#Attempted Questions
						if(len(SolvedQ.objects.filter(Q(q_id=question1.get(id_no=id1)) ,Q(id_no=request.user)))>0):
							score=SolvedQ.objects.filter(Q(id_no=request.user))
							return render(request, 'quizportal/attempted.html', {'id_no':id1})

			
						#Unattempted
						else:
							question=QuestionData.objects.filter(Q(id_no__exact=str(id_no)))
							args={'question':question,  'timer':h+":"+m+":"+time[2].split("+")[0]}
							return render(request, 'quizportal/questions.html', args)


#Scorecard
@login_required(login_url='login')
def score(request, id_no):
	score=SolvedQ.objects.filter(Q(id_no=request.user), Q(check=True))
	id1=User.objects.filter(Q(username=request.user)).values('username')
	return render(request, 'quizportal/score.html', {'score':len(score), 'id':id1, 'id_no':id_no})


#Ended
@login_required(login_url='login')
def ended(request):

	#Marking All Questions as Attempted
	question=QuestionData.objects.all()
	for i in question:
		if(SolvedQ.objects.filter(Q(id_no=request.user), Q(q_id=question.get(id_no=i.id_no)))):
			continue
		else:
			obj,notif=SolvedQ.objects.get_or_create(id_no=request.user, q_id=question.get(id_no=i.id_no), check=False)
			if notif is True:
				obj.save()

	#Getting Score
	score=SolvedQ.objects.filter(Q(id_no=request.user), Q(check=True))
	id1=User.objects.filter(Q(username=request.user)).values('username')
	return render(request, 'quizportal/ended.html', {'score':len(score), 'id':id1})


#Admin Only
def check_admin(user):
   return user.is_superuser


#Admin Main
@user_passes_test(check_admin)
def adminmain(request):
	return render(request, 'quizportal/adminmain.html')


#All Users' Details
@user_passes_test(check_admin)
def adminall(request):
	
	#Score of all Users
	scores=SolvedQ.objects.filter(Q(check=True))
	admindict={}
	for i in scores:
		username=User.objects.filter(Q(username=i.id_no)).values('username')
		for j in username:
			print(type(j['username']))
			if(j['username'] in admindict):
				admindict[j['username']]=(int)(admindict[j['username']])+1
			else:
				admindict[j['username']]=1

	return render(request, 'quizportal/adminall.html', {'allusers':admindict})


#CSV File Upload
@user_passes_test(check_admin)
def csvupload(request):
	if request.method == "POST":
		try:
			form = DataInput(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/adminmain')
		except:
			return HttpResponseRedirect(reverse('csvupload'))
	else:
		form = DataInput()
		context = {"form": form}
		return render(request, 'quizportal/csvupload.html', context)