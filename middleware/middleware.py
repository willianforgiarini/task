from .current_user import set_current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(getattr(request, "user", None)) # pega o atributo "user" do objeto request ou None
        response = self.get_response(request)
        return response
    
    # aṕos rodar o middleware ('middleware.middleware.CurrentUserMiddleware',) no settings
    # o método __call__ é chamado