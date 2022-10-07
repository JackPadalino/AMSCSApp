from django.db import models
from django.contrib.auth.models import User
from classroom.models import Classroom

grades = (
    (8,8),
    (9,9),
    (10,10),
    (11,11),
    (12,12)
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    classes = models.ManyToManyField(Classroom,blank=True,default=None,related_name='profiles')
    grade = models.IntegerField(choices=grades,default=0)
    solutions = models.IntegerField(default=0)
    image = models.ImageField(default='profile_pics/default.jpeg',upload_to='profile_pics/')
    #image = models.ImageField(default=None,upload_to='project_pics')

    #def get_absolute_url(self):
    #    return reverse('profile-details',kwargs={'pk':self.pk})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
