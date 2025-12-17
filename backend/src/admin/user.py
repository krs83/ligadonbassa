from sqladmin import ModelView
from backend.src.models import User


class UserAdmin(ModelView, model=User):
    column_list = "__all__"

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"
