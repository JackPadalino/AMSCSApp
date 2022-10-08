from django import forms
from django.apps import apps
from .models import Project,ProjectVideo,ProjectPhoto,ProjectComment

# form for students to join a new class
class JoinClassForm1(forms.Form):
    join_code = forms.CharField(label='Join code',max_length=10)

#~~~~~Project model forms~~~~~#
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description']
        labels = {
            'title':'Title | Give your project a title. Keep it short and sweet!',
            'description':'Description | Go all in and describe your project! Make sure you use CS vocabulary!'
        }

class ProjectLinkForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_link']
        labels = {
            'project_link':'Link | Add a link to your project (not required)'
        }

#~~~~~ProjectVideo model forms~~~~~#
class ProjectVideoForm(forms.ModelForm):
    class Meta:
        model = ProjectVideo
        fields = ['video']
        labels = {
            'video':'Project video | Add a video of your project in action (not required)'
        }

#~~~~~ProjectPhoto model forms~~~~~#
class ProjectPhotoForm(forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ['image']
        labels = {
            'image':'Project image | Add an image of your project or code (not required)'
        }

#~~~~~ProjectComment model forms~~~~~#
class CommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['content']
        labels = {
            'content':'Want to leave a comment? Remember to keep it positive and helpful!'
        }