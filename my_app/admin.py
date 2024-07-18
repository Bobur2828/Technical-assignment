from django.contrib import admin
from my_app.models.users import User
from my_app.models.article import Article

# Конфигурация административной панели для модели Article
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_first_name', 'public', 'created_at', 'updated_at')

    def author_first_name(self, obj):
        return obj.author.first_name

    author_first_name.admin_order_field = 'author__first_name'

admin.site.register(Article, ArticleAdmin)

# Конфигурация административной панели для модели User
class UserAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке записей модели User в административной панели
    list_display = ['email', 'user_role', 'is_staff']

# Регистрация модели User в административной панели с использованием конфигурации UserAdmin
admin.site.register(User, UserAdmin)
