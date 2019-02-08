from django.contrib import admin
from .models import QuestionData, Time, SolvedQ

admin.site.register(QuestionData)
admin.site.register(Time)
admin.site.register(SolvedQ)