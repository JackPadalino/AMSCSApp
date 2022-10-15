from django import forms
from django.apps import apps
from .models import Forum,ForumTopic,Question,Answer

'''
class JoinClassForm2(forms.Form):
    classroom = forms.ChoiceField(label='Join a class',choices=classoom_choices,required=True)
    join_code = forms.CharField(label='Join code',max_length=10,required=True)
'''

#~~~~~Question model form~~~~~#
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content','project_link']
        labels = {
            "content": "Content | Make sure you use CS vocabulary!",
            'project_link':'Link | Add a link to a project (not required)',
        }

#~~~~~Answer model form~~~~~#
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            "content": "Content | Remember to keep it positive and helpful!",
        }