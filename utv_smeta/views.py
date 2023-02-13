import re
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, DeleteView, ListView
from django.views.generic.edit import FormMixin

from utv_smeta.forms import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from utv_smeta.models import Cards, TableProject, EmployeeRate
from utv_smeta.service import CardService, WorkerService, CommentService, TableService


# Create your views here.


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'utv_smeta/register_user.html'
    success_message = 'Вы зарегестриваны!'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        ProfileUser.objects.create(user_id=self.object.pk)
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'utv_smeta/login.html'
    form_class = AuthenticationForm


class ProfileUserView(DetailView):
    model = ProfileUser
    template_name = 'utv_smeta/profile_user.html'


class UpdateProfileView(UpdateView):
    form_class = ProfileUserForm
    template_name = 'utv_smeta/profile_user_update.html'
    model = ProfileUser

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profileuser.pk})


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('regiister')


class HomeView(TemplateView):
    template_name = 'utv_smeta/base.html'


class CardsListView(View):
    def get(self, request, *args, **kwargs):
        cards = CardService(user_pk=self.request.user.pk).my_cards()
        return render(request, 'utv_smeta/cards.html', {'cards': cards})


class CardsCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'utv_smeta/cards_create.html', {'form': CardsCreateForm()})

    def post(self, request, *args, **kwargs):
        form = CardsCreateForm(request.POST)
        if form.is_valid():
            CardService(user_pk=self.request.user.pk, **form.cleaned_data).create_card()
            messages.success(request, 'Ваша карточка добавлена')
            return redirect('cards')
        return render(request, 'utv_smeta/cards_create.html', {'form': CardsCreateForm(request.POST)})


class CardUpdateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'utv_smeta/cards_update.html', {'form': CardsCreateForm()})

    def post(self, request, *args, **kwargs):
        form = CardsCreateForm(request.POST)
        if form.is_valid():
            CardService(request=request, card_pk=kwargs['card_pk'], **form.cleaned_data).update_card()
            messages.success(request, 'Ваша карточка изменена')
            return redirect('cards')
        return render(request, 'utv_smeta/cards_create.html', {'form': CardsCreateForm(request.POST)})


class CardDeleteView(View):
    def post(self, request, *args, **kwargs):
        CardService(card_pk=kwargs['card_pk']).delete_card()
        messages.success(request, 'Ваша карточка удалена')
        return redirect('cards')


class CardDetailView(View):

    def get(self, request, *args, **kwargs):
        w = WorkerService(card_pk=kwargs['card_pk'],
                          author_pk=request.user.pk).my_work()
        form = WorkerForm(instance=w)
        cont = {'cards': CardService(card_pk=kwargs['card_pk']).give_me_card(),
                'form_worker': form,
                'my_work': WorkerService(author_pk=request.user.pk, card_pk=kwargs['card_pk']).count_worker_in_card(),
                'form_comment': CommentCreateForm(),
                'form_table': TableForm()}
        return render(request, 'utv_smeta/cards_detail.html', context=cont)


class WorkerCreateView(View):
    def post(self, request, *args, **kwargs):
        form_worker = WorkerForm(request.POST)
        if form_worker.is_valid():
            WorkerService(author_pk=request.user.pk,
                          card_pk=kwargs['card_pk'],
                          **form_worker.cleaned_data).create_worker()
            messages.success(request, 'Работа над проектом началась')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return reverse_lazy('card_detail', kwargs['card_pk'], {'form_worker': WorkerForm(request.POST)})


class WorkerUpdateView(View):
    def post(self, request, *args, **kwargs):
        form_worker = WorkerForm(request.POST)
        if form_worker.is_valid():
            WorkerService(author_pk=request.user.pk,
                          card_pk=kwargs['card_pk'],
                          **form_worker.cleaned_data).update_worker()
            messages.success(request, 'Работа над проектом обновлена')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return reverse_lazy('card_detail', kwargs['card_pk'], {'form_worker': WorkerForm(request.POST)})


class WorkerDeleteView(View):
    def post(self, request, *args, **kwargs):
        WorkerService(author_pk=request.user.pk,
                      card_pk=kwargs['card_pk']).delete_worker()
        messages.success(request, 'Ваша работа над проектом удалена')
        return redirect('card_detail', card_pk=kwargs['card_pk'])


class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            CommentService(author_pk=request.user.pk, card_pk=kwargs['card_pk'], **form.cleaned_data).create_comment()
            messages.success(request, 'Комментарий добавлен')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return reverse_lazy('card_detail', kwargs['card_pk'], {'form_comment': CommentCreateForm(request.POST)})


class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        CommentService(comment_pk=request.POST['comment_pk'],
                       author_pk=request.user.pk,
                       card_pk=kwargs['card_pk']).delete_comment()
        messages.success(request, 'Ваш коментарий удалён')
        return redirect('card_detail', card_pk=kwargs['card_pk'])


class TableCreateView(View):
    def post(self, request, *args, **kwargs):
        form = TableForm(request.POST)
        if form.is_valid():
            t = TableService(request=request, card_pk=kwargs['card_pk'], **form.cleaned_data)
            if t.valid_table():
                t.create_table()
                messages.success(request, 'Таблица успешно создана')
                return redirect('card_detail', card_pk=kwargs['card_pk'])
        messages.error(request, 'У сотрудников не проставлена ЗП')
        return redirect('card_detail', card_pk=kwargs['card_pk'])


class TableDetailView(View):

    def get(self, request, *args, **kwargs):
        t = TableService(table_pk=kwargs['table_pk']).get_table()
        c = {'table': t,
             'form_table': TableUpdateForm(instance=t),
             'form_fact_table': TableUpdateFactForm(instance=t)}
        return render(request, 'utv_smeta/table.html', c)


class TablePlannedUpdateView(View):
    def post(self, request, *args, **kwargs):
        form = TableUpdateForm(request.POST)
        if form.is_valid():
            TableService(table_pk=kwargs['table_pk'], card_pk=kwargs['card_pk'], **form.cleaned_data).update_planned_table()
            return redirect('table_detail', card_pk=kwargs['card_pk'], table_pk=kwargs['table_pk'])


class TableUpdateView(View):
    def post(self, request, *args, **kwargs):
        form = TableUpdateFactForm(request.POST)
        if form.is_valid():
            TableService(table_pk=kwargs['table_pk'], card_pk=kwargs['card_pk'], **form.cleaned_data).update_table()
            return redirect('table_detail', card_pk=kwargs['card_pk'], table_pk=kwargs['table_pk'])
