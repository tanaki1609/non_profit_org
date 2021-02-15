from django.contrib import admin
from consultation.models import Question, AdminAnswer

admin.site.register(Question)
admin.site.register(AdminAnswer)