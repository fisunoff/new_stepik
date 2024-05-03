from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_tables2 import SingleTableView, SingleTableMixin

from lesson.models import Course, Block
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
    fields = ('name', 'description')
    success_url = reverse_lazy('course-list')


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'base_create.html'
    fields = ('name', 'description')

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


class CourseDeleteView(CreateView):
    model = Course
    success_url = reverse_lazy('course-list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())