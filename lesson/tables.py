import django_tables2 as tables

from .models import Course, Block


class CourseTable(tables.Table):
    # edit = tables.TemplateColumn('<a href="{% url \'course-detail\' record.id %}">&#128203;</a>', orderable=False,
    #                              verbose_name="")
    detail = tables.TemplateColumn(
        '''
        <a href="{% url 'course-detail' record.id %}">&#128203;</a>
        ''',
        orderable=False, verbose_name=""
    )

    actions = tables.TemplateColumn(
        '''
       {% if user.is_superuser or record.user_can_edit %}
        <a href="{% url 'course-update' record.id %}">&#9997;</a>
        <a href="{% url 'course-delete' record.id %}" onclick="return confirm('Точно хотите удалить?')">&#10060;</a>
        {% endif %}
        ''',
        orderable=False, verbose_name="Действия"
    )

    class Meta:
        model = Course
        template_name = "django_tables2/bootstrap.html"
        fields = ('detail', 'actions', 'name',)


class BlockTable(tables.Table):
    detail = tables.TemplateColumn(
        '''
        <a href="{% url 'course-detail' record.id %}">&#128203;</a>
        ''',
        orderable=False, verbose_name=""
    )

    actions = tables.TemplateColumn(
        '''
       {% if user.is_superuser or record.user_can_edit %}
        <a href="{% url 'course-update' record.id %}">&#9997;</a>
        <a href="{% url 'course-delete' record.id %}" onclick="return confirm('Точно хотите удалить?')">&#10060;</a>
        {% endif %}
        ''',
        orderable=False, verbose_name="Действия"
    )

    class Meta:
        model = Block
        template_name = "django_tables2/bootstrap.html"
        fields = ('detail', 'action', 'name',)
