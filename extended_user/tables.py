import django_tables2 as tables
from extended_user.models import Profile


class UserTable(tables.Table):
    edit = tables.TemplateColumn('<a href="{% url \'profile-detail\' record.id %}">&#128203;</a>', orderable=False,
                                 verbose_name="")

    class Meta:
        model = Profile
        template_name = "django_tables2/bootstrap.html"
        fields = ("edit", 'surname', 'name', 'patronymic')
