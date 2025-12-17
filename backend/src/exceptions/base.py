from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(BaseAppException):
    def __init__(self, detail: str = "Не найдено"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictException(BaseAppException):
    def __init__(self, detail: str = "Конфликт данных"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class AuthenticationException(BaseAppException):
    def __init__(self, detail: str = "Неверные учетные данные"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


