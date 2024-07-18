from django.urls import path
from my_app.views.article import *
from my_app.views.auth import *

urlpatterns = [
    # Для подписчиков: отображение всех статей
    path('view_all_articles/', ArticleListView.as_view(), name='для подписчиков'),
    
    # Для авторизованных пользователей: создание и просмотр собственных статей
    path('my_articles/', ArticleListCreateAPIView.as_view(), name='article-list-create'),
    
    # Для авторизованных пользователей: получение, обновление и удаление конкретной статьи
    path('my_articles/<int:pk>/', ArticleRetrieveUpdateDestroyAPIView.as_view(), name='article-detail'),
    
    # Регистрация нового пользователя
    path('auth/register/', register, name='register'),
    
    # Авторизация пользователя (вход в систему)
    path('auth/login/', custom_login, name='login'),
    
    # Выход пользователя из системы
    path('auth/logout/', log_out, name='logout'),
]
