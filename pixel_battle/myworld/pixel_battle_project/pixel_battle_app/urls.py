from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('notime/main', lambda req: redirect('/main/')),
    path('main/loginregister/main/', lambda req: redirect('/main/')),
    path('', lambda req: redirect('/main/')),
    path('main/main', views.main_page, name='main_page'),
    path('notime/', views.notime, name='notime'),
    path('main/', views.main_page, name='main_page'),
    path('main/loginregister', views.login_or_register, name="login_or_register"),
    path('main/sorry', views.sorry, name='sorry')
]

#django is hard :C