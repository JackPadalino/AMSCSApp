import re
import os
from itertools import chain
from django.urls.base import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    )
from .models import (
    Profile,
    )
from classroom.models import Classroom,Project,ProjectTopic,ProjectComment,ProjectCommentNotification
from .forms import JoinClassForm
from forum.models import (
    Answer,
    AnswerNotification,
    HelpfulNotification
)

EMAIL_DOMAIN = os.environ.get('EMAIL_DOMAIN')
REGISTERED_EMAILS = os.environ.get('REGISTERED_EMAILS')

# view to register a new user
def RegisterView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            email_domain = re.search("@[\w.]+", email)
            if email_domain.group() == EMAIL_DOMAIN:
            #if email in REGISTERED_EMAILS:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}! You are now able to sign in.')
                return redirect('users-login')
            else:
                messages.error(request,f'Sorry. You are not authorized to register.')
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request,'users/users-register.html',context)

# view to log in
def login(request):
    return render(request,'users/users-login.html')

# view to see/update details of a user's profile
@login_required
def ProfileView(request):
    user=request.user
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account information has been updated.')
            return redirect('users-my-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    classes = request.user.profile.classes.all()
    user_questions = len(request.user.questions.all())
    user_answers = len(request.user.answers.all())
    user_solutions = user.profile.solutions
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'classes':classes,
        'user_questions':user_questions,
        'user_answers':user_answers,
        'user_solutions':user_solutions
    }
    return render(request,'users/users-my-profile.html',context)

@login_required
def MyClassesListView(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    classes = profile.classes.all()
    context = {
        'classes':classes
    }
    return render(request,'users/users-my-classes.html',context)

@login_required
# view to join a class
def JoinClassView(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            classroom_pk = int(form.cleaned_data['classroom'])
            classroom = Classroom.objects.get(pk=classroom_pk)
            join_code = form.cleaned_data['join_code']
            if join_code == classroom.join_code:
                if profile not in classroom.profiles.all():
                    classroom.profiles.add(profile)
                    messages.add_message(request,messages.SUCCESS,'You have been added to this class. Welcome to the team!')
                else:
                    messages.add_message(request,messages.SUCCESS,'Looks like you are already in this class!')
                return redirect('users-my-classes')
            else:
                messages.add_message(request,messages.ERROR,'Oops! Something went wrong. Maybe you entered the wrong join code?')       
    else:
        form = JoinClassForm()
    
    context = {
        'form':form,
    }
    return render(request,'users/users-join-class.html',context)

@login_required
def MyProjectsListView(request):
    user = request.user
    projects = Project.objects.filter(user=user)
    context = {
        'projects':projects
    }
    return render(request,'users/users-my-projects.html',context)

@login_required
def NotificationsListView(request):
    user = request.user
    project_comment_notifications = ProjectCommentNotification.objects.filter(notified_user=user)
    answer_notifications = AnswerNotification.objects.filter(notified_user=user)
    helpful_notifications = HelpfulNotification.objects.filter(notified_user=user)
    context = {
        'project_comment_notifications':project_comment_notifications,
        'answer_notifications':answer_notifications,
        'helpful_notifications':helpful_notifications
    }
    return render(request,'users/users-notifications.html',context)