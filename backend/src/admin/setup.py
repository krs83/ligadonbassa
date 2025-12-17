from sqladmin import Admin
from backend.src.admin.auth import AdminAuth
from backend.src.admin.dependency import session_maker_admin
from backend.src.config import settings
from backend.src.database import engine
from backend.src.admin.user import UserAdmin
from backend.src.admin.athlete import AthleteAdmin
from backend.src.admin.tournament import TournamentAdmin
from backend.src.admin.athlete_tournament import AthleteTournamentLinkAdmin


def setup_admin(app) -> None:
    admin = Admin(
        app=app,
        engine=engine,
        session_maker=session_maker_admin,
        authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
        title=settings.SITENAME,
    )

    admin.add_view(UserAdmin)
    admin.add_view(AthleteAdmin)
    admin.add_view(TournamentAdmin)
    admin.add_view(AthleteTournamentLinkAdmin)
