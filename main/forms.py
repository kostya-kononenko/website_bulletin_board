from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from main.apps import user_registered
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, Comment
from captcha.fields import CaptchaField


class ChangeUserInfoForm(forms.ModelForm):
    """Форма для зміни особистих даних"""

    email = forms.EmailField(required=True, label="Адреса електронної пошти")

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_massage')


class RegisterUserForm(forms.ModelForm):
    """Форма для занесення інформації щодо нового користувача"""

    email = forms.EmailField(required=True, label='Адреса електронної пошти')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль(повторіть)', widget=forms.PasswordInput,
                                help_text='Введить будь ласка ще раз пароль для перевірки')

    def clean_password1(self):
        """Форма для валідації паролю"""

        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        """Форма для перевірка на співпадіння паролів"""

        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password1']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введені паролі не співпадають', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        """Форма для зберігання нового користувача та відправлення користувачу листа (user_registered)"""

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_massage')


class SubRubricForm(forms.ModelForm):
    """Форма для занесення назви надрубрик"""
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(), empty_label=None, label='Надрубрика',
                                          required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    """Форма для здійснення пошуку за введеним словом"""
    keywords = forms.CharField(required=False, max_length=20, label='')


class BbForm(forms.ModelForm):
    """Форма для введення користувачем оголошення"""
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


class UserCommentForm(forms.ModelForm):
    """Форма для коментування оголошення зареєстрованим користувачем"""

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    """Форма для коментування оголошення не зареєстрованим користувачем"""

    captcha = CaptchaField(label='Введіть текст з картинки', error_messages={'invalid': 'Невірний текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'bb': forms.HiddenInput}


