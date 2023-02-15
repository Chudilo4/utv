from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_flatpickr.widgets import DateTimePickerInput

from users.models import CustomUser
from utv_smeta.models import Cards, Comments, Worker, TableProject


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'avatar']


class UserCustomChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'avatar']


class CardsCreateForm(forms.ModelForm):
    class Meta:
        model = Cards
        fields = ['title', 'description', 'performers', 'deadline']
        widgets = {
            'deadline': DateTimePickerInput()
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