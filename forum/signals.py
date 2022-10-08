from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from classroom.models import Classroom,ProjectTopic
from .models import Forum,ForumTopic,Answer,AnswerNotification

@receiver(post_save,sender=Classroom)
def create_forum(sender,instance,created,**kwargs):
    if created:
        Forum.objects.create(title='Projects',classroom=instance)
        Forum.objects.create(title='Class Discussions',classroom=instance)

# signal to create a new forum topic every time a new project topic is created
@receiver(post_save,sender=ProjectTopic)
def create_forum(sender,instance,created,**kwargs):
    if created:
        forum = Forum.objects.get(title='Projects',classroom=instance.classroom)
        ForumTopic.objects.create(title=instance.title,forum=forum)

@receiver(post_save,sender=Answer)
def create_answer_notification(sender,instance,created,**kwargs):
    if created:
        AnswerNotification.objects.create(answer=instance,notified_user=instance.question.author)