from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
	# Quiz
    path('', LoginView.as_view(template_name='quizportal/login.html'), name="login"),
    path('detail/<id_no>', views.detail, name='detail'),
    path('score/<id_no>', views.score, name='score'),
    path('ended', views.ended, name='ended'),
    path('register', views.register, name='register'),
    path('admincsvupload', views.csvupload, name='csvupload'),
    path('adminmain', views.adminmain, name='adminmain'),
    path('adminall', views.adminall, name='adminall'),
    path('logout', LogoutView.as_view(template_name='quizportal/logout.html'), name="logout"),

]