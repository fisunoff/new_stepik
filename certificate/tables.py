import django_tables2 as tables

from certificate.models import Demand


class DemandTable(tables.Table):
    edit = tables.TemplateColumn('<a href="{% url \'demand-update\' record.course.id %}">&#128203;</a>', orderable=False,
                                 verbose_name="")

    class Meta:
        model = Demand
        template_name = "django_tables2/bootstrap.html"
        fields = ('edit', 'name', 'percent', )
