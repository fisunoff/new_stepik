import django_tables2 as tables
from .models import Course, Block


class CourseTable(tables.Table):
    edit = tables.TemplateColumn('<a href="{% url \'course-detail\' record.id %}">&#128203;</a>', orderable=False,
                                 verbose_name="")

    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ('edit', 'name', )


class BlockTable(tables.Table):
    class Meta:
        model = Block
        template_name = "django_tables2/bootstrap.html"
        fields = ('edit', 'name', )
