from rest_framework import serializers
from my_app.models.users import User

# Сериализатор для модели пользователя
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)  # Поле для подтверждения пароля, только для записи
    
    class Meta:
        model = User  # Используемая модель
        fields = ['first_name', 'email', 'password', 'confirm_password']  # Поля, которые будут включены в сериализатор

    def validate(self, data):
        email = data.get('email')  # Получаем значение email из данных
        password = data.get('password')  # Получаем значение пароля из данных
        confirm_password = data.get('confirm_password')  # Получаем значение подтверждения пароля из данных

        # Проверяем, что все обязательные поля заполнены
        if not email or not password or not confirm_password:
            raise serializers.ValidationError({"message": "Электронная почта, пароль и подтверждение пароля обязательны"})

        # Проверяем, совпадают ли пароль и подтверждение пароля
        if password != confirm_password:
            raise serializers.ValidationError({"message": "Пароль и подтверждение пароля не совпадают"})

        # Проверка формата электронной почты
        if '@' not in email:
            raise serializers.ValidationError({"message": "Неправильный формат электронной почты"})

        # Проверка длины пароля
        if len(password) < 8:
            raise serializers.ValidationError({"message": "Пароль должен содержать как минимум 8 символов"})

        # Проверка наличия хотя бы одной буквы в пароле
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError({"message": "Пароль должен содержать как минимум одну букву"})

        # Проверка существования пользователя с такой же электронной почтой
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "Электронная почта уже зарегистрирована"})

        return data  # Возвращаем проверенные данные

    def create(self, validated_data):
        password = validated_data.pop('password')  # Извлекаем пароль из проверенных данных
        user = User(email=validated_data['email'], first_name=validated_data.get('first_name', ''))  # Создаем нового пользователя с указанным email и first_name
        user.set_password(password)  # Устанавливаем пароль пользователя
        user.save()  # Сохраняем пользователя в базе данных
        return user  # Возвращаем созданного пользователя
