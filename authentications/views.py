from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, ChangePasswordSerializer, UserSerializer, UserDetailSerializer
from .permissions import IsSelfOrSuperUser


class UserListView(ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["username", "email"]

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSelfOrSuperUser]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        self.check_object_permissions(request, user) # percorre as permissões da view, se tiver o método "has_object_permission", esse método é chamado (request, obj)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        self.check_object_permissions(request, user)

        serializer = UserDetailSerializer(user, data=request.data, partial=True, context={"request": request}) # partial=True - não é obrigado enviar todos os camposs

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        self.check_object_permissions(request, user)

        user.delete()
        return Response({"message": "Usuário deleteado!"})

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data) # request.data, JSON da requisição
        # cria uma instancia do serializer, validando os dados passados

        if serializer.is_valid(): # verifica se os dados estão validos
            # se forem validos, armazena em serializer.validated_data
            serializer.save() # ativa o metodo create do serializer, que usa o validated_data
            return Response({"message": "Usuário registrado!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # serializer.erros - retorna os erros encontrados pelo serializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"message": "Senha atual incorreta."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"detail": "Senha atualizada."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        