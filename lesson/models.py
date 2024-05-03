from django.db import models

from utils.models import EditingModel, AuthoringModel


# Create your models here.
class Course(EditingModel):
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name
