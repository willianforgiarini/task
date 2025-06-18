from middleware.current_user import get_current_user
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core import serializers
from task.models import Tasks, Auditoria
from datetime import datetime
import json


@receiver(pre_save, sender=Tasks)
def serialize_pre_save(sender, instance, **kwargs):
    task = Tasks.objects.filter(id=instance.id).first()
    if task:
        instance.serialized_pre_save = serializers.serialize('json', [task])
    else:
        instance.serialized_pre_save = serializers.serialize('json', [instance])

@receiver(post_save, sender=Tasks)
def serialize_post_save(sender, instance, **kwargs):
    instance.serialized_post_data = serializers.serialize('json', [instance])

@receiver(post_save, sender=Tasks)
def log(sender, instance, created, **kwargs):
    user = get_current_user()
    if created:
        Auditoria.objects.create(
            table="Taks",
            description="Created",
            old_body={},
            new_body=json.loads(instance.serialized_pre_save),
            created_at=datetime.now(),
            created_by_user=user
        )
    else:
        Auditoria.objects.create(
            table="Taks",
            description="Updated",
            old_body=json.loads(instance.serialized_pre_save),
            new_body=json.loads(instance.serialized_post_data),
            created_at=datetime.now(),
            created_by_user=user
        )

@receiver(pre_delete, sender=Tasks)
def serialize_pre_delete(sender, instance, **kwargs):
    task = Tasks.objects.get(id=instance.id)
    instance.serialized_pre_delete = serializers.serialize('json', [task])

@receiver(post_delete, sender=Tasks)
def log_delete(sender, instance, **kwargs):
    Auditoria.objects.create(
        table="Task",
        description="Deleted",
        old_body=json.loads(instance.serialized_pre_delete),
        new_body={},
        created_at=datetime.now()
    )