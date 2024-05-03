from django import forms

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
        self.instance.profile = self.profile
        self.instance.task = self.task
        if self.task.autotest:
            self.instance.auto_test()
        super().save(commit)
