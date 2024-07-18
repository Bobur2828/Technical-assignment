from django.db import models
from .users import User

class Article(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок статьи'  # Поле для заголовка статьи. Ограничение в 255 символов.
    )
    content = models.TextField(
        verbose_name='Содержание статьи'  # Поле для содержания статьи. Текст любого размера.
    )
    public = models.BooleanField(
        verbose_name='Публичный доступ'  # Поле для определения доступности статьи для публичного просмотра (True/False).
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор статьи'  # Поле для связи статьи с пользователем. При удалении пользователя все его статьи также будут удалены.
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'  # Поле для хранения даты и времени создания статьи. Значение устанавливается автоматически при создании.
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего обновления'  # Поле для хранения даты и времени последнего обновления статьи. Значение обновляется автоматически при изменении.
    )

    def __str__(self):
        return self.title  # Метод для представления объекта модели в виде строки. Возвращает заголовок статьи.
