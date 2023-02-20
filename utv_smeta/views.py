from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView

from users.models import CustomUser
from utv_smeta.forms import (
    UserRegisterForm,
    CardsCreateForm,
    WorkerForm,
    CommentCreateForm,
    TableForm,
    TableUpdateForm,
    TableUpdateFactForm,
    UserCustomChangeForm)
from utv_smeta.models import Worker
from utv_smeta.service import CardService


# Create your views here.


class RegisterUserView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'utv_smeta/register_user.html'
    success_message = 'Вы зарегестриваны!'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class UserChangeView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserCustomChangeForm
    template_name = 'utv_smeta/update_user.html'
    success_message = 'Вы изменили профиль'
    success_url = reverse_lazy('home')


class LoginUserView(LoginView):
    template_name = 'utv_smeta/login.html'
    form_class = AuthenticationForm


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('regiister')


class HomeView(TemplateView):
    template_name = 'utv_smeta/base.html'


class CardsListView(View):
    def get(self, request, *args, **kwargs):
        cards = CardService(author=self.request.user.pk).my_cards()
        return render(request, 'utv_smeta/cards.html', {'cards': cards})


class CardsCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'utv_smeta/cards_create.html', {'form': CardsCreateForm()})

    def post(self, request, *args, **kwargs):
        context = {'form': CardsCreateForm(request.POST)}
        form = CardsCreateForm(request.POST)
        if form.is_valid():
            CardService(
                author=self.request.user.pk,
                **form.cleaned_data).create_card()
            messages.success(request, 'Ваша карточка добавлена')
            return redirect('cards')
        return render(request, 'utv_smeta/cards_create.html', context)


class CardUpdateView(View):

    def get(self, request, *args, **kwargs):
        card = CardService(card_pk=kwargs['card_pk'])
        context = {'form': CardsCreateForm(instance=card.give_me_card())}
        return render(request, 'utv_smeta/cards_update.html', context)

    def post(self, request, *args, **kwargs):
        context = {'form': CardsCreateForm(request.POST)}
        form = CardsCreateForm(request.POST)
        if form.is_valid():
            CardService(
                request=request,
                card_pk=kwargs['card_pk'],
                **form.cleaned_data).update_card()
            messages.success(request, 'Ваша карточка изменена')
            return redirect('cards')
        return render(request, 'utv_smeta/cards_create.html', context)


class CardDeleteView(View):
    def post(self, request, *args, **kwargs):
        CardService(card_pk=kwargs['card_pk']).delete_card()
        messages.success(request, 'Ваша карточка удалена')
        return redirect('cards')


class CardDetailView(View):
    def get(self, request, *args, **kwargs):
        card = CardService(card_pk=kwargs['card_pk'], author=request.user.pk)
        try:
            work = card.get_my_work()
            form = WorkerForm(instance=work)
        except Worker.DoesNotExist:
            form = WorkerForm()
            work = False
        cont = {'cards': card.give_me_card(),
                'form_worker': form,
                'my_work': work,
                'form_comment': CommentCreateForm(),
                'form_table': TableForm()}
        return render(request, 'utv_smeta/cards_detail.html', context=cont)


class WorkerCreateView(View):
    def post(self, request, *args, **kwargs):
        context = {'form_worker': WorkerForm(request.POST)}
        form_worker = WorkerForm(request.POST)
        if form_worker.is_valid():
            CardService(author=request.user.pk,
                        card_pk=kwargs['card_pk'],
                        **form_worker.cleaned_data).create_worker()
            messages.success(request, 'Работа над проектом началась')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return reverse_lazy('card_detail', kwargs['card_pk'], context)


class WorkerUpdateView(View):
    def post(self, request, *args, **kwargs):
        context = {'form_worker': WorkerForm(request.POST)}
        form_worker = WorkerForm(request.POST)
        if form_worker.is_valid():
            CardService(author=request.user.pk,
                        card_pk=kwargs['card_pk'],
                        **form_worker.cleaned_data).update_worker()
            messages.success(request, 'Работа над проектом обновлена')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return reverse_lazy('card_detail', kwargs['card_pk'], context)


class WorkerDeleteView(View):
    def post(self, request, *args, **kwargs):
        CardService(author=request.user.pk,
                    card_pk=kwargs['card_pk']).delete_worker()
        messages.success(request, 'Ваша работа над проектом удалена')
        return redirect('card_detail', card_pk=kwargs['card_pk'])


class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        context = {'form_comment': CommentCreateForm(request.POST)}
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            CardService(
                author=request.user.pk,
                card_pk=kwargs['card_pk'],
                **form.cleaned_data).create_comment()
            messages.success(request, 'Комментарий добавлен')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return reverse_lazy('card_detail', kwargs['card_pk'], context)


class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        CardService(comment_pk=request.POST['comment_pk'],
                    author=request.user.pk,
                    card_pk=kwargs['card_pk']).delete_comment()
        messages.success(request, 'Ваш коментарий удалён')
        return redirect('card_detail', card_pk=kwargs['card_pk'])


class TableCreateView(View):
    def post(self, request, *args, **kwargs):
        form = TableForm(request.POST)
        if form.is_valid():
            CardService(
                request=request,
                card_pk=kwargs['card_pk'],
                **form.cleaned_data
            ).create_table()
            messages.success(request, 'Таблица успешно создана')
            return redirect('card_detail', card_pk=kwargs['card_pk'])
        return redirect('card_detail', card_pk=kwargs['card_pk'])


class TableDetailView(View):

    def get(self, request, *args, **kwargs):
        table = CardService(table_pk=kwargs['table_pk'],
                            card_pk=kwargs['card_pk']).get_table()
        context = {'table': table,
                   'form_table': TableUpdateForm(instance=table),
                   'form_fact_table': TableUpdateFactForm(instance=table),
                   'card_pk': kwargs['card_pk']}
        return render(request, 'utv_smeta/table.html', context)


class TablePlannedUpdateView(View):
    def post(self, request, *args, **kwargs):
        form = TableUpdateForm(request.POST)
        if form.is_valid():
            CardService(
                table_pk=kwargs['table_pk'],
                card_pk=kwargs['card_pk'],
                **form.cleaned_data).update_planned_table()
            return redirect('table_detail', card_pk=kwargs['card_pk'], table_pk=kwargs['table_pk'])


class TableUpdateView(View):
    def post(self, request, *args, **kwargs):
        form = TableUpdateFactForm(request.POST)
        if form.is_valid():
            CardService(
                table_pk=kwargs['table_pk'],
                card_pk=kwargs['card_pk'],
                **form.cleaned_data).update_table()
            return redirect('table_detail', card_pk=kwargs['card_pk'], table_pk=kwargs['table_pk'])
