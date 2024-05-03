from django.urls import path, include

from extended_user.views import *

urlpatterns = [
    path('', UsersListView.as_view(), name="profile-list"),
    path('<int:pk>/', UserDetailView.as_view(), name='profile-detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='profile-update'),

]
