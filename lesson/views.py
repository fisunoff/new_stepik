from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_tables2 import SingleTableView, SingleTableMixin

from lesson.forms import AnswerForm, AnswerUpdateForm, TaskForm, CourseForm, TaskUpdateForm
from lesson.models import Course, Block, CourseRegister, Task, Answer
from lesson.tables import CourseTable, BlockTable


class CourseListView(SingleTableView):
    model = Course
    template_name = 'lesson/course/list.html'
    table_class = CourseTable

    def get_queryset(self):
        queryset = super().get_queryset()
        user_profile = None
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            for course in queryset:
                course.user_can_edit = self.request.user.is_superuser or course.can_edit(user_profile)
        return queryset
        # queryset = super().get_queryset()
        # if self.request.user.is_authenticated:
        #     user_profile = self.request.user.profile
        #     filtered_courses = [course.id for course in queryset if course.can_edit(user_profile)]
        #     print("Filtered courses:", filtered_courses)  # Вывод для отладки
        #     queryset = queryset.filter(id__in=filtered_courses)
        # return queryset

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile
            # Проверяем, является ли пользователь автором какого-либо курса (или имеет другие права для добавления)
            # context['user_can_create_course'] = Course.objects.filter(
            #     author=user_profile).exists() or user_profile.authoring
            context['user_can_create_course'] = user_profile.can_author
        else:
            context['user_can_create_course'] = False
        return context


class CourseCreateView(CreateView):
    model = Course
    template_name = 'base_create.html'
    fields = ('name', 'description', 'image')
    success_url = reverse_lazy('course-list')

    def form_valid(self, form):
        # Перемещаем проверку профиля на первое место
        user_profile = getattr(self.request.user, 'profile', None)
        if not user_profile:
            form.add_error(None, 'Ошибка: у пользователя нет профиля. Необходим профиль для создания курса.')
            return self.form_invalid(form)

        # Обработка файла перед сохранением объекта
        file = self.request.FILES.get('image')
        if file:
            print("File received: ", file.name)
        else:
            print("No file received")

        self.object = form.save(commit=False)
        self.object.author = user_profile
        self.object.save()
        form.save_m2m()  # Сохраняем связанные данные ManyToMany, если есть
        return HttpResponseRedirect(self.get_success_url())


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'base_create.html'

    def get_success_url(self):
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
        kwargs['can_get_cert'] = False
        if kwargs['registered']:
            reg = CourseRegister.objects.get(course=self.get_object(), profile=self.request.user.profile)
            kwargs['mark'] = reg.mark
            kwargs['percent'] = reg.percent
            kwargs['can_change'] = self.object.can_edit(self.request.user.profile)
            demands = self.object.demand_set.order_by('percent')
            if demands.exists():
                if demands.first().percent <= reg.percent:
                    kwargs['can_get_cert'] = True
        else:
            kwargs['mark'] = 0
            kwargs['percent'] = 0
            kwargs['can_change'] = False
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


class TaskCreateView(CreateView):
    model = Task
    template_name = 'base_create.html'
    form_class = TaskForm

    def get(self, request, from_pk, *args, **kwargs):
        self.block = get_object_or_404(Block, pk=from_pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, from_pk, *args, **kwargs):
        self.block = get_object_or_404(Block, pk=from_pk)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        task = Block.objects.get(pk=self.kwargs['from_pk']).task_set.first()
        return reverse_lazy('answer-create', kwargs={'from_pk': task.pk})

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['block'] = self.block
        kwargs['profile'] = self.request.user.profile
        return kwargs


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'base_create.html'


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'lesson/task/detail_answer.html'

    def get(self, request, from_pk, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=from_pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, from_pk, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=from_pk)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('answer-create', kwargs={'from_pk': self.task.pk})

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        kwargs = super().get_context_data(**kwargs)
        kwargs['task'] = self.task
        kwargs['best_try'] = self.task.best_try(profile=profile)
        if self.task.can_edit(profile):
            kwargs['answers_qs'] = self.task.answer_set.all()
        else:
            kwargs['answers_qs'] = self.task.answer_set.filter(author=profile)
        kwargs['can_edit'] = self.task.can_edit(profile)
        return kwargs

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['task'] = self.task
        kwargs['profile'] = self.request.user.profile
        return kwargs


class AnswerUpdateView(UpdateView):
    model = Answer
    template_name = 'lesson/task/answer_update.html'
    form_class = AnswerUpdateForm

    def get_success_url(self):
        answer = Answer.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('answer-create', kwargs={'from_pk': answer.task.pk})


class BlockCreateView(CreateView):
    model = Block
    template_name = 'base_create.html'
    fields = ('name', 'description')

    def get(self, request, from_pk, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=from_pk)
        return super().get(request, *args, **kwargs)

    def post(self, request, from_pk, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=from_pk)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Перемещаем проверку профиля на первое место
        user_profile = getattr(self.request.user, 'profile', None)
        if not user_profile:
            form.add_error(None, 'Ошибка: у пользователя нет профиля. Необходим профиль для создания курса.')
            return self.form_invalid(form)
        if not self.course.can_edit(user_profile):
            form.add_error(None, 'Ошибка: Недостаточно прав')
            return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.course = self.course
        self.object.author = user_profile
        self.object.save()
        form.save_m2m()  # Сохраняем связанные данные ManyToMany, если есть
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs=dict(pk=self.course.pk))


class BlockUpdateView(UpdateView):
    model = Block
    template_name = 'base_create.html'
    fields = ('name', 'description')

    def form_valid(self, form):
        # Перемещаем проверку профиля на первое место
        user_profile = getattr(self.request.user, 'profile', None)
        if not user_profile:
            form.add_error(None, 'Ошибка: у пользователя нет профиля. Необходим профиль для создания курса.')
            return self.form_invalid(form)
        if not self.object.course.can_edit(user_profile):
            form.add_error(None, 'Ошибка: Недостаточно прав')
            return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.last_editor = user_profile
        self.object.save()
        form.save_m2m()  # Сохраняем связанные данные ManyToMany, если есть
        return HttpResponseRedirect(self.get_success_url())
