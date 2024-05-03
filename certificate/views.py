from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django_tables2 import SingleTableView, SingleTableMixin

from certificate.models import Demand
from certificate.tables import DemandTable
from lesson.models import Course


class DemandListView(SingleTableMixin, DetailView):
    model = Course
    template_name = 'certificate/demand_list.html'
    table_class = DemandTable

    def get_table_data(self):
        return Demand.objects.filter(course=self.get_object())


class DemandCreateView(CreateView):
    model = Demand
    template_name = 'base_create.html'
    fields = ('name', 'percent', 'file')

    def get(self, request, pk, *args, **kwargs):
        self.pk = pk
        return super().get(request, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        self.pk = pk
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('demand-list', kwargs={'pk': self.pk})


class DemandUpdateView(UpdateView):
    model = Demand
    template_name = 'base_create.html'
    fields = ('name', 'percent', 'file')

    def get_success_url(self):
        return reverse_lazy('demand-list', kwargs={'pk': self.object.course.pk})
