from django.db import models

from lesson import const
from utils.models import EditingModel, AuthoringModel


# Create your models here.
class Course(EditingModel):
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    @property
    def demands_str(self):
        res = ''
        for demand in self.demand_set.all():
            res += f'{demand.name}: от {demand.percent}\n'
        res.strip('\n')
        return res


class Block(AuthoringModel):
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    course = models.ForeignKey(to=Course, verbose_name='Курс', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(AuthoringModel):
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    block = models.ForeignKey(to=Block, verbose_name='Блок', null=False, on_delete=models.CASCADE)
    correct_answer = models.TextField(verbose_name='Правильный ответ', null=True, blank=True)
    max_mark = models.IntegerField('Максимальный балл')
    need_file = models.BooleanField(verbose_name='Можно приложить файл', default=False)
    autotest = models.BooleanField(verbose_name='Автоматическая проверка', default=True)

    def __str__(self):
        return self.name


class Answer(AuthoringModel):
    status = models.CharField(max_length=127, choices=const.statuses, default=const.IN_PROGRESS)
    answer = models.TextField(verbose_name='Правильный ответ', null=True, blank=False)
    mark = models.IntegerField('Максимальный балл')
    task = models.ForeignKey(to=Task, null=False, on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Прикрепленный файл", blank=True, null=True, upload_to='media/')

    def __str__(self):
        return f'{self.answer} ({self.mark})'
