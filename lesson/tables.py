import django_tables2 as tables
from .models import Course, Block


class CourseTable(tables.Table):
    # edit = tables.TemplateColumn('<a href="{% url \'course-detail\' record.id %}">&#128203;</a>', orderable=False,
    #                              verbose_name="")
    actions = tables.TemplateColumn(
        '''
        <a href="{% url 'course-detail' record.id %}">&#9997;</a>
        <a href="{% url 'course-delete' record.id %}" onclick="return confirm('Точно хотите удалить?')">&#10060;</a>
        ''',
        orderable=False,
        verbose_name="Действия"
    )

    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ('actions', 'name', )


class BlockTable(tables.Table):
    class Meta:
        model = Block
        template_name = "django_tables2/bootstrap.html"
        fields = ('edit', 'name', )
