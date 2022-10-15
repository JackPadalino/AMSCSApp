from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from classroom.models import (
    Classroom
    )

# forum model
class Forum(models.Model):
    title = models.CharField(max_length=100,default=None)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='forums')

    #def get_absolute_url(self):
    #    return reverse('forum-details',kwargs={'pk':self.category.pk})

    def __str__(self):
        return f'{self.classroom} - {self.title}'

# topic model
class ForumTopic(models.Model):
    title = models.CharField(max_length=100,default=None)
    description = models.TextField(max_length=500,null=True,default=None)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE,related_name='forum_topics')

    #def get_absolute_url(self):
    #    return reverse('topic-details',kwargs={'pk':self.category.pk})

    def __str__(self):
        return f'{self.forum.classroom.title} - {self.forum.title} - {self.title}'

# question model
class Question(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='questions')
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE,related_name='questions')
    forum_topic = models.ForeignKey(ForumTopic,on_delete=models.CASCADE,related_name='questions')
    #title = models.CharField(max_length=100,default=None)
    content = models.TextField(max_length=500)
    project_link = models.CharField(max_length=1000,blank=True,default=None)
    date_posted = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('forum-questions-list',kwargs={'pk':self.forum_topic.pk})

    def __str__(self):
        return f"{self.forum_topic.title} - {self.author.first_name} {self.author.last_name} - {self.date_posted}"

# answer model
class Answer(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='answers')
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE,related_name='answers')
    forum_topic = models.ForeignKey(ForumTopic,on_delete=models.CASCADE,default=None,related_name='answers')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    content = models.TextField(max_length=500)
    requested = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    solution = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('forum-question-details',kwargs={'pk':self.question.pk})

    def __str__(self):
        if self.solution == True:
            return f" {self.question.title} - {self.author.first_name} {self.author.last_name} - {self.date_posted} - MARKED AS SOLUTION"
        else:
            return f"{self.question.title} - {self.author.first_name} {self.author.last_name} - {self.date_posted}"

# answer notification model
class AnswerNotification(models.Model):
    answer = models.OneToOneField(Answer,on_delete=models.CASCADE)
    notified_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='answer_notifications')
    #viewed = models.BooleanField(default=False)

    #def get_absolute_url(self):
    #    return reverse('answer-notification-details',kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.answer.author.first_name} {self.answer.author.last_name} responded to {self.answer.question.author.first_name} {self.answer.question.author.last_name}'s question"

class HelpfulNotification(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    notified_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='helpful_notifications')

    def __str__(self):
        return f"{self.answer.question.author.first_name} {self.answer.question.author.last_name} marked {self.answer.author.first_name} {self.answer.author.last_name}'s answer as helpful."
