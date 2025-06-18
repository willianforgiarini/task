from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.generics import ListAPIView
from middleware.mixins import CurrentUserMixin
from .serializers import TasksSerializer, AuditoriaSerializer
from .permissions import IsAdminCreateOrUserTaskUpdateOrReadOnly
from .paginations import SimplePageNumberPagination
from .models import Tasks, Auditoria
from datetime import datetime


class TaskViewSet(CurrentUserMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminCreateOrUserTaskUpdateOrReadOnly]
    queryset = Tasks.objects.all().order_by("id")
    serializer_class = TasksSerializer
    filterset_fields = ["user", "title", "status", "created_at"]
    pagination_class = SimplePageNumberPagination

    def list(self, request, *args, **kwargs): # altera o metodo de listagem
        if "page" not in request.query_params:
            self.pagination_class = None # caso não seja passado page na URL, remove classe de paginação e retorna todas as task
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs): # altera o metodo de atualização
        instance = self.get_object() # retorna o objeto correto

        instance.updated_at = datetime.now()
        instance.save(update_fields=["updated_at"])
        
        return super().update(request, *args, **kwargs)

    @action(methods=["PUT"], detail=True, url_path="completed")
    def completed(self, request, pk):
        task = self.get_object()

        if task.status == "Concluída":
            return Response({"message": f"Tarefa ({task.title}) já está concluída."}, status=status.HTTP_400_BAD_REQUEST)

        task.status = "Concluída"
        task.completed_at = datetime.now()
        task.save(update_fields=["status"])

        return Response({"message": f"Tarefa ({task.title}) concluída com sucesso."})
    
    @action(methods=["PUT"], detail=True, url_path=r"add-user/(?P<user_id>\d+)")
    def add_user(self, request, pk, user_id):
        task = self.get_object()
        user = get_object_or_404(User, id=user_id)
        
        task.user = user
        task.save()

        return Response({"message": f"Usuário ({user.username}) atribuído à tarefa ({task.title})."})


class AuditoriaListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Auditoria.objects.all().order_by("id")
    serializer_class = AuditoriaSerializer