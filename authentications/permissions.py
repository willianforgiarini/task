from rest_framework.permissions import BasePermission


class IsSelfOrSuperUser(BasePermission):
    # permissão para somente o superuser ou o proprio usuário da requisição ter acesso as infos gerais do usuário
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_superuser