from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import TimestampedModel, AuthoringModel


# Create your models here.

class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=50, blank=False, null=True)
    surname = models.CharField("Фамилия", max_length=50, blank=False, null=True)
    patronymic = models.CharField("Отчество", max_length=50, blank=True, null=True)
    bio = models.TextField("Описание профиля", max_length=500, blank=True, null=True)
    post = models.CharField(verbose_name="Должность", max_length=200, blank=True, null=True)
    department = models.ForeignKey(to='extended_user.Department', verbose_name='Структурное подразделение',
                                   null=True, blank=True, on_delete=models.SET_NULL)
    communication = models.CharField(verbose_name="Контакты", max_length=200, blank=True, null=True)
    photo = models.ImageField(verbose_name="Фото профиля", blank=True, null=True)

    manager = models.BooleanField(verbose_name='Менеджер', default=False)
    authoring = models.BooleanField(verbose_name='Составитель курсов', default=False)

    def __str__(self):
        return f"{self.surname} {self.name}{' ' + self.patronymic if self.patronymic else ''}"

    @property
    def is_manager(self):
        return self.manager or self.user.is_superuser

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = ['name', 'surname', 'patronymic']
        # ordering = ['surname', 'name', 'position']


class Department(AuthoringModel):
    head = models.ForeignKey(to='extended_user.Department', verbose_name='Головное подразделение',
                             null=True, blank=True, on_delete=models.SET_NULL)
    chief = models.ForeignKey(to=Profile, verbose_name='Начальник', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='departments_by_chief')

    def can_edit(self, profile: Profile) -> bool:
        """Может ли сотрудник получать статистику по структурному подразделению"""
        head = self.head
        visited = set()
        if profile.is_manager:
            return True
        while head is not None:
            if head.pk in visited:
                return False  # Цикл
            if head.chief == Profile:
                return True
            visited.add(head.pk)
        return False

    class Meta:
        verbose_name = 'структурное подразделение'
        verbose_name_plural = 'структурные подразделения'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
