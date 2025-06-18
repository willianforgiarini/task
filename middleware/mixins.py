from .current_user import set_current_user

# Mixins - são classes auxiliares usadas para adicionar funcionalidades a outras classes, sem ser a classe principal.
# No Django, são muito usados em views para adicionar comportamentos reutilizáveis.
class CurrentUserMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        set_current_user(request.user)

# Mixins - classe para ser herdada junto com outras, adicionando funcionalidades específicas, mas não sendo usada sozinha.
