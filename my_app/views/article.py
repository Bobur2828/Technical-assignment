from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from my_app.models import Article
from my_app.serializers.articleSR import ArticleSerializer
from rest_framework.exceptions import PermissionDenied, NotFound

# Представление для получения списка статей
class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer  # Используемый сериализатор для представления
    authentication_classes = [BasicAuthentication]  # Использование базовой аутентификации
    permission_classes = [AllowAny]  # Доступно любому пользователю, включая неаутентифицированных

    def get_queryset(self):
        # Если пользователь аутентифицирован, возвращаем все статьи
        if self.request.user.is_authenticated:
            return Article.objects.all()
        else:
            # Если пользователь не аутентифицирован, возвращаем только публичные статьи
            return Article.objects.filter(public=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Получаем набор данных
        serializer = self.get_serializer(queryset, many=True)  # Сериализуем данные
        return Response({
            "status": "success",
            "data": {
                "articles": serializer.data
            }
        })

# Представление для получения списка статей и создания новой статьи
class ArticleListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]  # Использование базовой аутентификации
    permission_classes = [IsAuthenticated]  # Доступно только аутентифицированным пользователям
    serializer_class = ArticleSerializer  # Используемый сериализатор для представления

    def get_queryset(self):
        user = self.request.user
        # Если пользователь автор, возвращаем только его статьи
        if user.user_role == 'author':
            return Article.objects.filter(author=user)
        else:
            # Возвращаем пустой набор данных, если пользователь не имеет права создавать статьи
            return Article.objects.none()

    def post(self, request, *args, **kwargs):
        # Проверяем, имеет ли пользователь права для создания статьи
        if request.user.user_role != 'author':
            return Response({"status": "fail", "data": {"message": "У вас нет прав на создание статьи"}}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()  # Клонируем данные запроса
        data['author'] = request.user.id  # Устанавливаем автора статьи
        serializer = self.get_serializer(data=data)  # Создаем сериализатор с новыми данными
        if serializer.is_valid():  # Проверяем валидность данных
            serializer.save()  # Сохраняем данные статьи
            return Response({"status": "success", "data": {"article": serializer.data}}, status=status.HTTP_201_CREATED)
        # Возвращаем ошибки, если данные невалидны
        return Response({"status": "fail", "data": {"errors": serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)

# Представление для получения, обновления и удаления конкретной статьи
class ArticleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]  # Использование базовой аутентификации
    permission_classes = [IsAuthenticated]  # Доступно только аутентифицированным пользователям
    serializer_class = ArticleSerializer  # Используемый сериализатор для представления

    def get_queryset(self):
        user = self.request.user
        try:
            # Если пользователь автор, возвращаем только его статьи
            if user.user_role == 'author':
                return Article.objects.filter(author=user)
            else:
                # Если пользователь не автор, генерируем исключение о недостаточности прав
                raise PermissionDenied("У вас нет прав на создание статьи.")
        except Exception as e:
            # Возвращаем ответ с ошибкой в случае исключения
            return Response({"status": "fail", "data": {"message": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        try:
            obj = super().get_object()  # Получаем объект статьи
        except Article.DoesNotExist:
            # Возвращаем ответ с ошибкой, если статья не найдена
            return Response({"status": "fail", "data": {"message": "Статья не найдена или она вам не принадлежит."}}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем права пользователя на изменение статьи
        if self.request.user.user_role != 'author' or self.request.user != obj.author:
            raise PermissionDenied("У вас нет прав на изменение этой статьи.")

        return obj

    def put(self, request, *args, **kwargs):
        try:
            article = self.get_object()  # Получаем объект статьи
            if request.user.user_role != 'author' or request.user != article.author:
                # Проверяем права пользователя на изменение статьи
                return Response({"status": "fail", "data": {"message": "У вас нет прав для изменения этой статьи."}}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(article, data=request.data, partial=True)  # Создаем сериализатор с частичными данными
            if serializer.is_valid():  # Проверяем валидность данных
                serializer.save()  # Сохраняем обновленные данные
                return Response({"status": "success", "data": {"article": serializer.data}}, status=status.HTTP_200_OK)

            # Возвращаем ошибки, если данные невалидны
            return Response({"status": "fail", "data": {"errors": serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as e:
            # Возвращаем ответ с ошибкой в случае недостаточности прав
            return Response({"status": "fail", "data": {"message": str(e)}}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Возвращаем ответ с ошибкой для прочих исключений
            return Response({"status": "fail", "data": {"message": f"Ошибка: {str(e)}"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            article = self.get_object()  # Получаем объект статьи
            article.delete()  # Удаляем статью
            return Response({"status": "success", "data": {"message": "Статья успешно удалена."}}, status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            # Возвращаем ответ с ошибкой, если статья не найдена
            return Response({"status": "fail", "data": {"message": "Статья не найдена."}}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            # Возвращаем ответ с ошибкой, если у пользователя нет прав на удаление статьи
            return Response({"status": "fail", "data": {"message": "У вас нет прав на удаление этой статьи."}}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Возвращаем ответ с ошибкой для прочих исключений
            return Response({"status": "fail", "data": {"message": f"Ошибка: {str(e)}"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
