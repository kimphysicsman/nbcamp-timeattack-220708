from django.contrib import admin
from django.urls import path, include
from .views import SkillView, JobView, ApplicationView

urlpatterns = [
    path('', SkillView.as_view()),

    path('job', JobView.as_view()),
    path('apply', ApplicationView.as_view()),
]
