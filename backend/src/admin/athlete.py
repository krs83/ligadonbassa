from sqladmin import ModelView

from backend.src.models import Athlete


class AthleteAdmin(ModelView, model=Athlete):
    column_list = [Athlete. place, Athlete.fullname, Athlete.category, Athlete.academy, Athlete.affiliation, Athlete.points]
    # form_columns = [Athlete.fullname, Athlete.birth, Athlete.city, Athlete.region,Athlete.points]

    form_excluded_columns = [Athlete.id, Athlete.place]
    form_include_pk = True

    form_ajax_refs = {
        "tournaments":{
            "fields": ("title", "smoothcomp_date"),
            "order_by": ("smoothcomp_date",),
        }
    }

    column_labels = {
        "fullname": "Фамилия Имя",
        "category": "Категория",
        "academy": "Академия",
        "affiliation": "Аффилиация",
        "points": "Баллы",
        "place": "Место в рейтинге",
        "tournaments": "Турниры"
    }

    name = "Спортсмен"
    name_plural = "Спортсмены"
    icon = "fa-solid fa-person-walking"

    page_size = 50
