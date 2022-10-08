from django.contrib import admin
from .models import (
    Forum,
    ForumTopic,
    Question,
    Answer,
    AnswerNotification,
    HelpfulNotification
    )

admin.site.register(Forum)
admin.site.register(ForumTopic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerNotification)
admin.site.register(HelpfulNotification)