from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django_tables2 import SingleTableView, SingleTableMixin

from certificate import const
from certificate.generation import gen_document
from certificate.models import Demand, GeneratedDocument
from certificate.tables import DemandTable
from lesson.models import Course, CourseRegister


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


def update_certificate(request, course_pk):
    profile = request.user.profile
    course = Course.objects.get(pk=course_pk)
    has_percent = CourseRegister.objects.get(profile=profile, course=course).percent
    for demand in course.demand_set.order_by('-percent'):
        if demand.percent <= has_percent:
            new_doc = GeneratedDocument.objects.create(
                demand=demand,
                status=const.in_progress,
                course=course,
                percent=has_percent,
                author=profile,
            )
            gen_document(new_doc.id)
            GeneratedDocument.objects.filter(author=profile, demand__course=course).exclude(pk=new_doc.pk).delete()
            doc = GeneratedDocument.objects.get(pk=new_doc.id)
            return FileResponse(doc.document, as_attachment=True, filename=doc.document.name)
    return HttpResponse(status=400)
