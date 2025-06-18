from django.db import models
from django.contrib.auth.models import User


CHOICES = [
    ("Concluída", "Concluída"),
    ("Não concluída", "Não concluída"),
    ("Em andamento", "Em andamento"),
    ("Revisão", "Revisão")
]

class Tasks(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CHOICES, default="Não concluída")
    user = models.ForeignKey(User, related_name="my_tasks", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_data = models.DateField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

class Auditoria(models.Model):
    table = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_by_user = models.ForeignKey(User, related_name="my_user", on_delete=models.CASCADE, blank=True, null=True)
    new_body = models.CharField(max_length=255, blank=True, null=True)
    old_body = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
