from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django_flatpickr.widgets import DateTimePickerInput
from django import forms
from django.conf import settings

from utv_smeta.models import ProfileUser, Cards, Comments, Worker, TableProject


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['avatar']


class CardsCreateForm(forms.ModelForm):
    class Meta:
        model = Cards
        fields = ['title', 'description', 'performers', 'date_dedlain']
        widgets = {
            'date_dedlain': DateTimePickerInput()
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'row': 20,
                                           'cols': 40,
                                           'class': "form-control"
                                           },
                                    )
        }
        labels = {
            'text': 'Введите ваш комит!'
        }


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['actual_time', 'scheduled_time']


class TableForm(forms.ModelForm):
    class Meta:
        model = TableProject
        fields = ['planed_actors_salary', 'planned_other_expenses', 'planned_buying_music',
                  'planned_travel_expenses', 'planned_fare']


class TableUpdateForm(forms.ModelForm):
    class Meta:
        model = TableProject
        fields = ['price_client', 'planed_actors_salary', 'planned_other_expenses', 'planned_buying_music',
                  'planned_travel_expenses', 'planned_fare']


class TableUpdateFactForm(forms.ModelForm):
    class Meta:
        model = TableProject
        fields = ['price_client', 'actors_salary', 'other_expenses', 'buying_music',
                  'travel_expenses', 'fare']