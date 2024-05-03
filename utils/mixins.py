from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableMixin

from extended_user.models import Profile


class AddTitleFormMixin(FormMixin):
    title = None
    editing = False

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title or "Нет названия"
        kwargs['editing'] = self.editing
        return super().get_context_data(**kwargs)


class ProDetailView(DetailView):
    def title(self):
        return self.object.title

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.title or "Нет названия"
        can_edit = False
        if self.request.user.is_authenticated:
            can_edit = self.request.user.profile.pk == self.object.creator_id or self.request.user.is_superuser
        kwargs['can_edit'] = can_edit
        return super().get_context_data(**kwargs)


class DetailWithSingleTable(SingleTableMixin, ProDetailView):
    object_list = None
    table_model = None

    def get_table_data(self):
        return self.table_model.objects.all()


class SaveEditorMixin:
    save_creator_only = False

    def form_valid(self, form):
        self.object = form.save()
        user_profile = Profile.objects.get(id=self.request.user.profile.id)
        if not self.save_creator_only:
            self.object.last_editor = user_profile
        if not self.object.creator:
            self.object.creator = user_profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
