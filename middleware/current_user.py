import threading


_user = threading.local() # Uma variável thread-local é uma variável cujo valor é único para cada thread(request)

def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, "value", None)

# Thread-local é uma forma de armazenar dados que são específicos para cada thread (linha de execução) do seu programa.
# No Django, cada requisição HTTP geralmente é tratada por uma thread diferente.
# Usando thread-local, você garante que o dado (no caso, o usuário autenticado) não será compartilhado entre requisições diferentes, mesmo que ocorram ao mesmo tempo.