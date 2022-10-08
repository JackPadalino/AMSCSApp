from django.contrib import admin
from .models import (
    SchoolYear,
    Classroom,
    ProjectTopic,
    Project,
    ProjectPhoto,
    ProjectVideo,
    ProjectComment,
    ProjectCommentNotification
    )

admin.site.register(SchoolYear)
admin.site.register(Classroom)
admin.site.register(ProjectTopic)
admin.site.register(Project)
admin.site.register(ProjectPhoto)
admin.site.register(ProjectVideo)
admin.site.register(ProjectComment)
admin.site.register(ProjectCommentNotification)