from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Asosiy sahifalar
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # Kategoriyalar
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    
    # O'yinlar
    path('games/', views.game_list, name='game_list'),
    path('game/<slug:slug>/', views.game_detail, name='game_detail'),
    
    # Qidiruv
    path('search/', views.search, name='search'),
    
    # Aloqa
    path('contact/', views.contact, name='contact'),
    
    # Foydalanuvchi autentifikatsiyasi
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]
