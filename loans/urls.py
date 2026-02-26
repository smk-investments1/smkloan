from django.urls import path
from .views import home, login_page, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
]
