from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup),
    path('signup_page/', TemplateView.as_view(template_name = 'signup.html'), name='signup'),
    path('new_post_page/', TemplateView.as_view(template_name = 'make_post.html'), name= 'make_post'),
    path('new_post/', views.new_post, name='new_post'),
    path('list_posts/', views.list_posts, name='list_posts'),
    path('check_post/<int:key>', views.check_post, name='check_post'),
    path('delete_post/<int:key>', views.delete_post, name='delete_post'),
]