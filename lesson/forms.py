from django import forms

from lesson import const
from lesson.models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', ]

    def __init__(self, profile, task, *args, **kwargs):
        self.profile = profile
        self.task = task
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.author = self.profile
        self.instance.task = self.task
        if self.task.autotest:
            self.instance.auto_test()
        super().save(commit)


class AnswerUpdateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['mark', ]

    def clean_mark(self):
        mark = self.cleaned_data['mark']
        if mark > self.instance.task.max_mark or mark < 0:
            raise ValueError('Некорректное значение оценки')
        return mark

    def save(self, commit=True):
        self.instance.status = const.DONE
        super().save(commit)
