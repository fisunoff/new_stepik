import uuid

from django.db import models
from django.core.files import File
from certificate import const
from utils.models import AuthoringModel


# Create your models here.
class Demand(AuthoringModel):
    name = models.CharField(max_length=255, )
    course = models.ForeignKey('lesson.Course', on_delete=models.CASCADE, verbose_name='Курс', null=True)
    # qualification = будет позже
    percent = models.IntegerField(verbose_name='Требуемое количество процентов')
    file = models.FileField(null=True, blank=True, verbose_name='Файл шаблона')

    class Meta:
        verbose_name = "вариант сертификата"
        verbose_name_plural = "варианты сертификатов"
        ordering = ('-course', '-percent')


class GeneratedDocument(AuthoringModel):
    statuses = (
        (const.in_progress, const.in_progress),
        (const.OK, const.OK),
        (const.error, const.error),
        (const.warning, const.warning)
    )
    demand = models.ForeignKey(to=Demand, on_delete=models.PROTECT, verbose_name='Основание')
    document = models.FileField(upload_to="files/", null=True, blank=True, verbose_name='Файл')
    status = models.CharField(max_length=1024, verbose_name='Статус', choices=statuses, default='in_progress')
    error = models.CharField(null=False, blank=False, default='', max_length=4096)
    course = models.ForeignKey(to='lesson.Course', on_delete=models.SET_NULL, null=True)
    last_operation_time = models.DateTimeField('Последнее изменение', blank=True, null=True)
    last_version = models.BooleanField('Последняя версия', default=True)
    warnings = models.TextField('Предупреждения', null=True, blank=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ('-last_operation_time', )

    def set_document(self, path, name):
        self.document = File(open(path, 'rb'))
        ext = path.split('.')[-1]
        self.document.name = "%s.%s" % (uuid.uuid4(), ext)
        self.document.verbose_name = name
        self.save()
