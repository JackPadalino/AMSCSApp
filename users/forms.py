from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.apps import apps

#~~~~~User model forms~~~~~#
# here we are inheriting the user creating form that comes with Django, but we are adding the email field so 
# we can validate a user using their email
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

# this will create a form that will allow a user to update their profile information
# a model form creates a form that is able to interact with a specific model
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

#~~~~~Profile model forms~~~~~#
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['grade','image']
        labels = {
            'image':'Profile photo'
        }

# creating a list of classroom tuples for the JoinClassForm
classroom_app_models = apps.all_models['classroom']
classroom_models = classroom_app_models['classroom']
classrooms = classroom_models.objects.all()
classoom_choices = [(None,'-')]
for classroom in classrooms:
    classroom_tup = (str(classroom.pk),f'{classroom.title} {classroom.school_year}')
    classoom_choices.append(classroom_tup)
classroom_choices = tuple(classoom_choices)

class JoinClassForm(forms.Form):
    classroom = forms.ChoiceField(label='Join a class',choices=classoom_choices,required=True)
    join_code = forms.CharField(label='Join code',max_length=10,required=True)