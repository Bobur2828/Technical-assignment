from django.db import models  # Импортируем модуль для работы с моделями Django
from django.contrib.auth.models import AbstractUser  # Импортируем базовый класс для пользовательских моделей из Django
from django.contrib.auth.models import BaseUserManager  # Импортируем базовый менеджер пользователей из Django

# Определяем менеджер для модели пользователя
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Метод для создания обычного пользователя
        if not email:
            raise ValueError('The Email field must be set')  # Проверка наличия электронной почты
        email = self.normalize_email(email)  # Нормализация электронной почты (приведение к единому виду)
        user = self.model(email=email, **extra_fields)  # Создание объекта пользователя с указанными полями
        user.set_password(password)  # Установка пароля для пользователя
        user.save(using=self._db)  # Сохранение пользователя в базе данных
        return user  # Возвращение созданного пользователя

    def create_superuser(self, email, password=None, **extra_fields):
        # Метод для создания суперпользователя (администратора)
        extra_fields.setdefault('is_staff', True)  # Установка флага is_staff в True для суперпользователя
        extra_fields.setdefault('is_superuser', True)  # Установка флага is_superuser в True для суперпользователя
        extra_fields.setdefault('user_role', User.ADMIN)  # Установка роли пользователя в ADMIN для суперпользователя

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')  # Проверка, что is_staff установлено в True
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  # Проверка, что is_superuser установлено в True

        return self.create_user(email, password, **extra_fields)  # Создание суперпользователя с помощью метода create_user


# Определяем константы для ролей пользователя
FOLLOWER, AUTHOR, ADMIN = ('follower', 'author', 'admin')

class User(AbstractUser):
    # Определяем роли пользователя
    FOLLOWER = 'follower'
    AUTHOR = 'author'
    ADMIN = 'admin'

    USER_ROLES = (
        (FOLLOWER, FOLLOWER),
        (AUTHOR, AUTHOR),
        (ADMIN, ADMIN)
    )

    username = None  # Убираем поле username, так как мы используем email для аутентификации
    first_name = models.CharField(max_length=30)  
    email = models.EmailField(unique=True)  # Поле для хранения электронной почты, должно быть уникальным
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default=FOLLOWER)  # Поле для хранения роли пользователя

    objects = UserManager()  # Используем наш кастомный менеджер для модели User

    USERNAME_FIELD = 'email'  # Указываем, что для аутентификации используется поле email
    REQUIRED_FIELDS = []  # Список обязательных полей для создания суперпользователя (оставляем пустым, так как используем email)

    def __str__(self):
        return self.email  # Возвращаем строковое представление объекта модели в виде электронной почты
