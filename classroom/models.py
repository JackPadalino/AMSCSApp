from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.models import User

# school year model
class SchoolYear(models.Model):
    year = models.CharField(max_length=10,default='1900-1901')

    #def get_absolute_url(self):
    #    return reverse('school_year-details',kwargs={'pk':self.pk})

    def __str__(self):
        return f'{self.year}'

# classroom model
class Classroom(models.Model):
    title = models.CharField(max_length=50,default='My Classroom')
    school_year = models.ForeignKey(SchoolYear,on_delete=models.CASCADE,related_name='classrooms')
    #students = models.ManyToManyField(User,blank=True,default=None,related_name='classooms')
    image = models.ImageField(blank=True,default=None,null=True)
    join_code = models.CharField(max_length=10,default='abc123')
    
    #def get_absolute_url(self):
    #    return reverse('classroom-details',kwargs={'pk':self.pk})

    def __str__(self):
        return f'{self.title} - {self.school_year}'

# project topic model
class ProjectTopic(models.Model):
    title = models.CharField(max_length=100,default=None)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,related_name='project_topics')

    #def get_absolute_url(self):
    #    return reverse('topic-details',kwargs={'pk':self.pk})

    def __str__(self):
        return f'{self.classroom.title} - {self.title}'

class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='projects')
    project_topic = models.ForeignKey(ProjectTopic,on_delete=models.CASCADE,related_name='projects')
    title = models.CharField(max_length=50)
    description = models.TextField()
    project_link = models.URLField(max_length=1000,default=None,blank=True,null=True)
    temp = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('classroom-project-details',kwargs={'project_pk':self.pk})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.title}'

class ProjectPhoto(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='project_photos')
    image = models.ImageField(default=None,upload_to='project_pics/')

    def __str__(self):
        return f'{self.project}'

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='project_videos')
    video = models.CharField(max_length=1000,default=None)
    
    def get_absolute_url(self):
        return reverse('classroom-project-details',kwargs={'pk':self.project.pk})

    def __str__(self):
        return f'{self.project}'

class ProjectComment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()

    def get_absolute_url(self):
        return reverse('classroom-project-details',kwargs={'project_pk':self.project.pk})

    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name} commented on {self.project.user.first_name} {self.project.user.last_name}'s project"

class ProjectCommentNotification(models.Model):
    comment = models.OneToOneField(ProjectComment,on_delete=models.CASCADE)
    notified_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_notifications')

    #def get_absolute_url(self):
    #    return reverse('comment-notification-details',kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.comment.author} commented on {self.comment.project.user.first_name} {self.comment.project.user.last_name}'s project."