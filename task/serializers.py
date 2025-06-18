from rest_framework import serializers
from authentications.serializers import UserSerializer
from .models import Tasks, Auditoria


class TasksSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tasks
        fields = "__all__"


class AuditoriaSerializer(serializers.ModelSerializer):
    created_by_user = UserSerializer()

    class Meta:
        model = Auditoria
        fields = "__all__"