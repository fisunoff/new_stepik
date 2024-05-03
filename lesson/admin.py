from django.db.models import Q
from django import forms
from django.contrib import admin

from extended_user.models import Profile
from .models import *


class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseAdminForm, self).__init__(*args, **kwargs)
        self.fields['editors'].queryset = Profile.objects.filter(
            Q(manager=True) | Q(authoring=True)  # Фильтрация по manager или authoring
        )


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm


admin.site.register(Course, CourseAdmin)
admin.site.register(Block)
admin.site.register(Task)