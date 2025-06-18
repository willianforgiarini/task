from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserDetailSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "last_name", "email", "is_active", "date_joined", "first_name", "is_superuser"]

    def update(self, instance, validated_data):
        request = self.context.get("request")

        # somente o superuser pode alterar o campo is_superuser de outros usuários
        if "is_superuser" in self.initial_data and not request.user.is_superuser: # self.inital_data, contém o Body da requisição
            raise serializers.ValidationError({"message": "Você não tem permissão para alterar este campo!"})

        return super().update(instance, validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # write_only=True - somente recebe o campo, nunca retorna

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    # função que é chamada quando é usado o serializer para criar um objeto
    def create(self, validated_data): # validated_data já possui os dados validados de acordo com seu tipo
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"]) # salva a senha em hash
        user.save()
        return user
    

class ChangePasswordSerializer(serializers.Serializer): # classe base genérica, não está ligada a nem uma Model
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
