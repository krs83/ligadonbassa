from backend.src.exceptions.base import NotFoundException, ConflictException


class UserIDNotFoundException(NotFoundException):
    USER_ID_NOT_FOUND_TEXT = "Пользователь с ID №{} не найден"

    def __init__(self, user_id: int):
        super().__init__(detail=self.USER_ID_NOT_FOUND_TEXT.format(user_id))

class UserEmailNotFoundException(NotFoundException):
    USER_EMAIL_NOT_FOUND_TEXT = "Пользователь {} не найден"

    def __init__(self, email_id: str):
        super().__init__(detail=self.USER_EMAIL_NOT_FOUND_TEXT.format(email_id))

class UserConflictException(ConflictException):
    USER_CONFLICT_TEXT = "Пользователь {} уже существует"

    def __init__(self,  email: str):
        super().__init__(detail=self.USER_CONFLICT_TEXT.format(email))