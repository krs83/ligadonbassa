from sqladmin import ModelView

from backend.src.models import AthleteTournamentLink


class AthleteTournamentLinkAdmin(ModelView, model=AthleteTournamentLink):
    column_list = "__all__"
