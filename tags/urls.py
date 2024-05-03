from django.urls import path, include

from .views import *

urlpatterns = [
    path('', tags_view, name='tags'),
]
