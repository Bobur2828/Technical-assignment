from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from my_app.models import User
from my_app.serializers.userSR import UserSerializer

# Представление для аутентификации пользователя (вход в систему)
@api_view(['POST'])  # Поддерживает только POST-запросы
@authentication_classes([BasicAuthentication])  # Использование базовой аутентификации
@permission_classes([AllowAny])  # Доступно любому пользователю, включая неаутентифицированных
def custom_login(request):
    email = request.data.get('email')  # Получение email из данных запроса
    password = request.data.get('password')  # Получение пароля из данных запроса

    if not email or not password:  # Проверка на наличие email и пароля
        return Response({"status": "fail", "data": {"message": "Email и пароль не введены"},"input":{"email":"","password":""}}, status=status.HTTP_400_BAD_REQUEST)

    # Аутентификация пользователя по email и паролю
    user = authenticate(request, username=email, password=password)

    if user is not None:  # Проверка успешности аутентификации
        login(request, user)  # Вход в систему, если аутентификация успешна
        return Response({"status": "success", "data": {"message": "Авторизация успешна"}}, status=status.HTTP_200_OK)
    else:
        return Response({"status": "fail", "data": {"message": "Неверные учетные данные"}}, status=status.HTTP_401_UNAUTHORIZED)

# Представление для выхода из системы
@api_view(['POST'])  # Поддерживает только POST-запросы
@authentication_classes([BasicAuthentication])  # Использование базовой аутентификации
@permission_classes([IsAuthenticated])  # Доступно только аутентифицированным пользователям
def log_out(request):
    logout(request)  # Выход из системы
    return Response({"status": "success", "data": {"message": "Выход успешен"}}, status=status.HTTP_200_OK)

# Представление для регистрации нового пользователя
@api_view(['POST'])  # Поддерживает только POST-запросы
@authentication_classes([BasicAuthentication])  # Использование базовой аутентификации
@permission_classes([AllowAny])  # Доступно любому пользователю, включая неаутентифицированных
def register(request):
    serializer = UserSerializer(data=request.data)  # Создание экземпляра сериализатора с данными запроса
    
    if serializer.is_valid():  # Проверка валидности данных
        serializer.save()  # Сохранение данных пользователя
        return Response({"status": "success", "data": {"message": "Регистрация прошла успешно", "email": serializer.validated_data['email']}}, status=status.HTTP_201_CREATED)
    
    return Response({"status": "fail", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Возврат ошибок в случае некорректных данных
