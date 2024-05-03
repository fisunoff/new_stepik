from django.db import models

from lesson import const
from utils.models import EditingModel, AuthoringModel, TimestampedModel


# Create your models here.
class Course(EditingModel):
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Обложка', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def demands_str(self):
        res = ''
        for demand in self.demand_set.all():
            res += f'{demand.name}: от {demand.percent}\n'
        res.strip('\n')
        return res

    @property
    def rating(self):
        import random
        return random.randint(1, 5)

    @property
    def max_mark(self):
        return sum(b.max_mark for b in self.block_set.all())


class Block(AuthoringModel):
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    course = models.ForeignKey(to=Course, verbose_name='Курс', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def max_mark(self):
        return sum(self.task_set.values_list('max_mark', flat=True))

    def can_edit(self, profile) -> bool:
        return self.course.can_edit(profile)


class Task(AuthoringModel):
    '''
        answer_options =
        [
          {"id": 1, "text": "Вариант ответа№1"},
          {"id": 2, "text": "Вариант ответа№2"},
          {"id": 3, "text": "Вариант ответа№3"},
        ]

        correct_options =
        {
          "correact_ids": [1,3]
        }
    '''
    name = models.CharField(max_length=1024, null=False, blank=False, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    block = models.ForeignKey(to=Block, verbose_name='Блок', null=False, on_delete=models.CASCADE)
    correct_answer = models.TextField(verbose_name='Правильный ответ (текст)', null=True, blank=True)
    answer_options = models.TextField(verbose_name='Варианты ответа', null=True, blank=True)
    correct_options_answer = models.TextField(verbose_name='Правильный ответ (из вариантов)', null=True, blank=True)
    max_mark = models.IntegerField('Максимальный балл')
    need_file = models.BooleanField(verbose_name='Можно приложить файл', default=False)
    autotest = models.BooleanField(verbose_name='Автоматическая проверка', default=True)
    type = models.CharField(choices=const.task_types, verbose_name='Тип задачи', default=const.TEXT, max_length=127)

    def __str__(self):
        return self.name

    def best_try(self, profile):
        trys = Answer.objects.filter(task=self, author=profile).order_by('-mark')
        if trys.exists():
            return trys.first().mark
        return 0

    def can_edit(self, profile) -> bool:
        return self.block.can_edit(profile)

    def get_correct_radio_answer(self):
        pass


class Answer(AuthoringModel):
    status = models.CharField(max_length=127, choices=const.statuses, default=const.IN_PROGRESS)
    answer = models.TextField(verbose_name='Ответ', null=True, blank=False)
    mark = models.IntegerField('Балл')
    task = models.ForeignKey(to=Task, null=False, on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Прикрепленный файл", blank=True, null=True, upload_to='media/')

    def __str__(self):
        return f'{self.answer} ({self.mark})'

    def auto_test(self):
        if self.answer.lower() == self.task.correct_answer.lower():
            self.mark = self.task.max_mark
        else:
            self.mark = 0
        self.status = const.DONE

    def evaluate_answer(self):
        # Получаем правильные ответы
        correct_answers = self.task.correct_answer['correct_ids']
        # Проверяем, содержится ли ответ студента среди правильных
        if int(self.answer) in correct_answers:
            return self.task.max_mark
        return 0

    def can_edit(self, profile) -> bool:
        return self.task.can_edit(profile)


class CourseRegister(TimestampedModel):
    profile = models.ForeignKey(to='extended_user.Profile', on_delete=models.CASCADE, null=False, blank=False,
                                verbose_name='Пользователь')
    course = models.ForeignKey(to=Course, null=False, blank=False, on_delete=models.CASCADE,
                               verbose_name='Курс')

    @property
    def mark(self):
        return sum(i.mark or 0 for i in Answer.objects.filter(task__block__course=self.course, author=self.profile)) or 0

    @property
    def percent(self):
        if self.course.max_mark:
            return round(self.mark / self.course.max_mark * 100, 0)
        return 0
