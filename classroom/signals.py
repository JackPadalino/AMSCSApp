from django.db.models.signals import post_save
from django.dispatch import receiver
from classroom.models import ProjectComment,ProjectCommentNotification

@receiver(post_save,sender=ProjectComment)
def create_comment_notification(sender,instance,created,**kwargs):
    if created:
        ProjectCommentNotification.objects.create(comment=instance,notified_user=instance.project.user)