from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import (
    Forum,
    ForumTopic,
    Question,
    Answer,
    AnswerNotification,
    HelpfulNotification
    )
from .forms import (
    QuestionForm,
    AnswerForm
)

# Create your views here.
@login_required
def ForumTopicsListView(request,pk):
    forum=Forum.objects.get(pk=pk)
    forum_topics=forum.forum_topics.all()
    classroom=forum.classroom
    context={
        'forum':forum,
        'forum_topics':forum_topics,
        'classroom':classroom
    }
    return render(request,'forum/forum-topics-list.html',context)

@login_required
def QuestionsListView(request,forum_topic_pk):
    forum_topic=ForumTopic.objects.get(pk=forum_topic_pk)
    questions=forum_topic.questions.all()
    context={
        'forum_topic':forum_topic,
        'questions':questions
    }
    return render(request,'forum/forum-questions-list.html',context)

@login_required
def AskQuestionView(request,forum_topic_pk):
    user=request.user
    forum_topic=ForumTopic.objects.get(pk=forum_topic_pk)
    forum=forum_topic.forum
    # display error message if student has not yet joined class
    if user.profile not in forum.classroom.profiles.all():
        messages.error(request,f'Sorry. Only students who have joined this class can ask questions!')
        return redirect('forum-questions-list',forum_topic_pk=forum_topic.pk)
    else:
        if request.method == 'POST':
                form = QuestionForm(request.POST)
                if form.is_valid():
                    question = form.save(commit=False)
                    question.author=user
                    question.forum=forum
                    question.forum_topic=forum_topic
                    question.title=form.cleaned_data['title']
                    question.content=form.cleaned_data['content']
                    question.save()
                    return redirect('forum-questions-list',forum_topic_pk=forum_topic.pk)
        else:
            form = QuestionForm()
        context = {
            'form':form
        }
        return render(request,'forum/forum-ask-new-question.html',context)

# view to see the details of a question
@login_required
def QuestionDetailsView(request,question_pk):
    user=request.user
    question = Question.objects.get(pk=question_pk)
    answers=question.answers.all()
    context = {
        'question':question,
        'answers':answers,
    }
    return render(request,'forum/forum-question-details.html',context)

# view to edit the text of a question
@login_required
def EditQuestionView(request,question_pk):
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            form.save()
            return redirect('forum-question-details',question_pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    context = {
        'form':form,
        'question':question
    }
    return render(request,'forum/forum-edit-question.html',context)

@login_required
def QuestionConfirmDeleteView(request,question_pk):
    question = Question.objects.get(pk=question_pk)
    context = {
        'question':question,
    }
    return render(request,'forum/forum-question-confirm-delete.html',context)

# view to delete a question
@login_required
def QuestionDeleteView(request,question_pk):
    question = Question.objects.get(pk=question_pk)
    forum_topic=question.forum_topic
    question.delete()
    return redirect('forum-questions-list',forum_topic_pk=forum_topic.pk)

@login_required
def QuestionsListView(request,forum_topic_pk):
    forum_topic=ForumTopic.objects.get(pk=forum_topic_pk)
    questions=forum_topic.questions.all()
    context={
        'forum_topic':forum_topic,
        'questions':questions
    }
    return render(request,'forum/forum-questions-list.html',context)

@login_required
def AnswerView(request,question_pk):
    user=request.user
    question=Question.objects.get(pk=question_pk)
    forum_topic=question.forum_topic
    forum=forum_topic.forum
    if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author=user
                answer.forum=forum
                answer.forum_topic=forum_topic
                answer.question=question
                answer.content=form.cleaned_data['content']
                answer.save()
                return redirect('forum-question-details',question_pk=question.pk)
    else:
        form = AnswerForm()
    context = {
        'form':form,
        'question':question
    }
    return render(request,'forum/forum-answer-question.html',context)

# view to edit the text of an answer
@login_required
def EditAnswerView(request,answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    if request.method == "POST":
        form = AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            form.save()
            return redirect('forum-question-details',question_pk=answer.question.pk)
    else:
        form = AnswerForm(instance=answer)
    context = {
        'form':form,
        'answer':answer
    }
    return render(request,'forum/forum-edit-answer.html',context)

@login_required
def AnswerConfirmDeleteView(request,answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    question = answer.question
    context = {
        'answer':answer,
        'question':question
    }
    return render(request,'forum/forum-answer-confirm-delete.html',context)

# view to delete a question
@login_required
def AnswerDeleteView(request,answer_pk):
    answer = Answer.objects.get(pk=answer_pk)
    answer.delete()
    return redirect('forum-question-details',question_pk=answer.question.pk)

def AnswerNotificationDeleteView(request,notification_pk):
    notification=AnswerNotification.objects.get(pk=notification_pk)
    question=notification.answer.question
    notification.delete()
    return redirect('forum-question-details',question_pk=question.pk)

def RequestHelpfulNotificationView(request,answer_pk):
    answer=Answer.objects.get(pk=answer_pk)
    superusers=User.objects.filter(is_superuser=True)
    if answer.reviewed == True:
        pass
    else:
        if answer.requested:
            answer.requested=False
            HelpfulNotification.objects.filter(answer=answer).delete()
        else:
            answer.requested=True
            for user in superusers:
                HelpfulNotification.objects.create(answer=answer,notified_user=user)
        answer.save()
    return redirect('forum-question-details',question_pk=answer.question.pk)

def ApproveDenyHelpfulRequestView(request,notification_pk,decision):
    notification=HelpfulNotification.objects.get(pk=notification_pk)
    question=notification.answer.question
    answer=notification.answer
    users=[question.author,answer.author]
    if decision=='approve':
        answer.solution=True
        for user in users:
            user.profile.solutions+=1
            user.profile.save()
            HelpfulNotification.objects.create(answer=answer,notified_user=user)
    answer.reviewed=True
    answer.save()
    notification.delete()
    if request.user.is_superuser:
        return redirect('users-my-notifications')
    else:
        return redirect('forum-question-details',question_pk=question.pk)

# view to handle notifications for non-superusers
def HelpfulNotificationDeleteView(request,notification_pk):
    notification=HelpfulNotification.objects.get(pk=notification_pk)
    question=notification.answer.question
    notification.delete()
    if request.user.is_superuser:
        return redirect('users-my-notifications')
    else:
        return redirect('forum-question-details',question_pk=question.pk)