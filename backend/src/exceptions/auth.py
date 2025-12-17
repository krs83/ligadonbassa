from backend.src.exceptions.base import AuthenticationException


class AuthFailedException(AuthenticationException):
    AUTH_FAILED_TEXT = "Вы ввели неверный email или пароль"

    def __init__(self):
        super().__init__(detail=self.AUTH_FAILED_TEXT)

