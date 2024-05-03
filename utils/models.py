from django.db import models


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    edited = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class AuthoringModel(TimestampedModel):
    author = models.ForeignKey(to='extended_user.Profile', on_delete=models.CASCADE,
                               null=True, blank=True, verbose_name='Автор', related_name='%(class)s_by_author')
    last_editor = models.ForeignKey(to='extended_user.Profile', on_delete=models.CASCADE,
                                    null=True, blank=True, verbose_name='Автор последних изменений',
                                    related_name='%(class)s_by_editors')

    class Meta:
        abstract = True

    def can_edit(self, profile) -> bool:
        """Может редактировать"""
        if profile.is_manager:
            return True
        if profile == self.author:
            return True
        return False


class EditingModel(AuthoringModel):
    editors = models.ManyToManyField(to='extended_user.Profile', verbose_name='Могут редактировать')

    class Meta:
        abstract = True

    def can_edit(self, profile) -> bool:
        """Может редактировать"""
        if super().can_edit(profile):
            return True
        if profile in self.editors.all():
            return True
        return False
