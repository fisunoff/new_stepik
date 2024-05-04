from django import forms
from lesson import const
from lesson.models import Answer, Task, Course
from ckeditor.widgets import CKEditorWidget


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label="Описание")

    class Meta:
        model = Course
        fields = ['name', 'description', 'image']
        labels = {
            'name': 'Название курса',
            'image': 'Изображение курса'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'type', 'correct_answer', 'max_mark')

    def __init__(self, profile, block, *args, **kwargs):
        self.profile = profile
        self.block = block
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.author = self.profile
        self.instance.block = self.block
        super().save(commit)
