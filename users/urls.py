from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
from .views import AddUserView, UserDeleteView, UserProfileView, UsersListView,UserEditView,MarinaView,UsersInMarinaView
urlpatterns =[
    path('',MarinaView.as_view(), name='marinas'),
    path('marina/<int:marina_id>/',UsersInMarinaView.as_view(), name='users_in_marina'),
    path('add/',AddUserView.as_view(), name='add_user'),
    path('<int:pk>/',UserProfileView.as_view(), name='user_profile'),
    path('users/<int:pk>/edit/', UserEditView.as_view(), name='edit_user'),  # New URL for editing users
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html',authentication_form=CustomAuthenticationForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),    
]