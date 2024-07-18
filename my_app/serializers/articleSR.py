from rest_framework import serializers
from my_app.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)  # Добавляем поле для имени автора

    class Meta:
        model = Article
        fields = ['id','title', 'content', 'public', 'author_first_name', 'created_at', 'updated_at']
