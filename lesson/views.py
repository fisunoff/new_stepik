from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_tables2 import SingleTableView, SingleTableMixin

from lesson.models import Course, Block, CourseRegister, Task
from lesson.tables import CourseTable, BlockTable


# Create your views here.
class CourseListView(SingleTableView):
    model = Course
    template_name = 'lesson/course/list.html'
    table_class = CourseTable

    def get_queryset(self):
        return Course.objects.all()
        # return Class.objects.filter(event_id=self.request.GET.get('event_id'))


class CourseCreateView(CreateView):
    model = Course
    template_name = 'base_create.html'
    fields = ('name', 'description', 'image')
    success_url = reverse_lazy('course-list')


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'base_create.html'
    fields = ('name', 'description', 'image')

    def get_success_url(self):
        # self.object.time_edit = timezone.now()
        # self.object.save()
        return reverse_lazy('course-list')


class CourseDetailView(SingleTableMixin, DetailView):
    model = Course
    template_name = 'lesson/course/detail.html'
    table_class = BlockTable

    def get_table_data(self):
        qs = Block.objects.filter(course=self.get_object())
        return qs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['registered'] = CourseRegister.objects.filter(course=self.get_object(),
                                                             profile=self.request.user.profile).exists()
        if kwargs['registered']:
            reg = CourseRegister.objects.get(course=self.get_object(), profile=self.request.user.profile)
            kwargs['mark'] = reg.mark
            kwargs['percent'] = reg.percent
        else:
            kwargs['mark'] = 0
            kwargs['percent'] = 0
        return kwargs


class CourseDeleteView(CreateView):
    model = Course
    success_url = reverse_lazy('course-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class CourseRegistrationView(CreateView):
    model = Course

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        CourseRegister.objects.update_or_create(course=self.object, profile=request.user.profile)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.object.pk})


class TaskDetailView(DetailView):
    model = Task
    template_name = 'lesson/course/detail.html'