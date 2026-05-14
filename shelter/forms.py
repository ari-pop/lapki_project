from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import AdoptionApplication, Feedback, News, OwnerQuestionnaire, Pet


YES_NO_CHOICES = ((True, 'Да'), (False, 'Нет'))


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get('class', '').strip()
            field.widget.attrs['class'] = f'{css_class} form-control'.strip()
            if field.required and field.label and not field.label.endswith(' *'):
                field.label = f'{field.label} *'
                field.widget.attrs['data-required'] = 'true'


class FeedbackForm(StyledModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'message': 'Сообщение',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'rows': 5}),
        }


class AdoptionApplicationForm(StyledModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['phone', 'city', 'housing_type', 'experience']:
            self.fields[name].required = True
            self.fields[name].help_text = ''
        self.fields['why_adopt'].required = False
        self.fields['why_adopt'].help_text = ''
        if self.fields['why_adopt'].label.endswith(' *'):
            self.fields['why_adopt'].label = self.fields['why_adopt'].label[:-2]

    class Meta:
        model = AdoptionApplication
        fields = [
            'full_name',
            'email',
            'phone',
            'age',
            'city',
            'housing_type',
            'has_other_pets',
            'has_children',
            'experience',
            'why_adopt',
        ]
        labels = {
            'full_name': 'ФИО',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'age': 'Возраст',
            'city': 'Город',
            'housing_type': 'Тип жилья',
            'has_other_pets': 'Есть другие животные',
            'has_children': 'Есть дети',
            'experience': 'Опыт содержания животных',
            'why_adopt': 'Почему хотите взять питомца',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Ваше ФИО'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ваш телефон'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Ваш возраст'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ваш город'}),
            'housing_type': forms.TextInput(attrs={'placeholder': 'Квартира, дом, съёмное жильё и т.д.'}),
            'experience': forms.Textarea(attrs={'placeholder': 'Кратко опишите ваш опыт', 'rows': 4}),
            'why_adopt': forms.Textarea(attrs={'placeholder': 'Почему вы хотите взять питомца?', 'rows': 4}),
        }


class OwnerQuestionnaireForm(StyledModelForm):
    has_pet_experience = forms.TypedChoiceField(
        required=False,
        label='Был ли у вас раньше питомец',
        choices=YES_NO_CHOICES,
        coerce=lambda value: value == 'True',
        widget=forms.RadioSelect(attrs={'class': 'quiz-options'}),
        initial=None,
    )
    has_children = forms.TypedChoiceField(
        label='Есть дети',
        choices=YES_NO_CHOICES,
        coerce=lambda value: value == 'True',
        widget=forms.RadioSelect(attrs={'class': 'quiz-options'}),
        initial=None,
    )
    has_other_pets = forms.TypedChoiceField(
        label='Есть другие животные',
        choices=YES_NO_CHOICES,
        coerce=lambda value: value == 'True',
        widget=forms.RadioSelect(attrs={'class': 'quiz-options'}),
        initial=None,
    )
    ready_for_medical_care = forms.TypedChoiceField(
        label='Готов(а) ухаживать за питомцем с особенностями здоровья',
        choices=YES_NO_CHOICES,
        coerce=lambda value: value == 'True',
        widget=forms.RadioSelect(attrs={'class': 'quiz-options'}),
        initial=None,
    )
    contact_email = forms.EmailField(
        required=False,
        label='Электронная почта для сохранения анкеты',
        help_text='Необязательно. По этой почте можно сохранить результаты в кабинет.',
        widget=forms.EmailInput(attrs={'placeholder': 'Ваш email'}),
    )

    def __init__(self, *args, **kwargs):
        self.user_is_authenticated = kwargs.pop('user_is_authenticated', False)
        super().__init__(*args, **kwargs)

        self.fields['experience_years'].required = False
        self.fields['experience_years'].help_text = ''
        self.fields['pet_age_preference'].required = True
        self.fields['pet_age_preference'].help_text = ''
        self.fields['pet_gender_preference'].required = True
        self.fields['pet_gender_preference'].help_text = ''
        self.fields['additional_info'].required = False
        self.fields['additional_info'].help_text = ''

        radio_fields = [
            'housing_type',
            'activity_level',
            'time_at_home',
            'pet_preference',
            'pet_age_preference',
            'pet_gender_preference',
            'adoption_goal',
        ]
        for name in radio_fields:
            filtered_choices = [
                (value, label)
                for value, label in self.fields[name].choices
                if str(value).strip() not in {'', 'None'}
            ]
            self.fields[name].choices = filtered_choices
            self.fields[name].widget = forms.RadioSelect(
                attrs={'class': 'quiz-options'},
                choices=filtered_choices,
            )

        experience_initial = self.initial.get('experience_years', 0) or 0
        self.fields['experience_years'].initial = experience_initial
        self.fields['has_pet_experience'].initial = (
            'True' if experience_initial >= 1 else 'False'
        ) if 'experience_years' in self.initial or 'has_pet_experience' in self.initial else None
        self.fields['has_children'].initial = 'True' if self.initial.get('has_children') is True else 'False' if self.initial.get('has_children') is False else None
        self.fields['has_other_pets'].initial = 'True' if self.initial.get('has_other_pets') is True else 'False' if self.initial.get('has_other_pets') is False else None
        self.fields['ready_for_medical_care'].initial = 'True' if self.initial.get('ready_for_medical_care') is True else 'False' if self.initial.get('ready_for_medical_care') is False else None
        self.fields['pet_preference'].initial = self.initial.get('pet_preference', 'any')
        self.fields['pet_age_preference'].initial = self.initial.get('pet_age_preference', 'any')
        self.fields['pet_gender_preference'].initial = self.initial.get('pet_gender_preference', 'any')
        self.fields['adoption_goal'].initial = self.initial.get('adoption_goal', 'any')

        if self.user_is_authenticated:
            self.fields.pop('contact_email', None)

    def clean_experience_years(self):
        if not self.cleaned_data.get('has_pet_experience'):
            return 0
        value = self.cleaned_data.get('experience_years')
        return 1 if value in (None, '') else value

    class Meta:
        model = OwnerQuestionnaire
        fields = [
            'full_name',
            'age',
            'city',
            'housing_type',
            'has_children',
            'has_other_pets',
            'experience_years',
            'activity_level',
            'time_at_home',
            'pet_preference',
            'pet_age_preference',
            'pet_gender_preference',
            'adoption_goal',
            'ready_for_medical_care',
            'additional_info',
        ]
        labels = {
            'full_name': 'ФИО',
            'age': 'Возраст',
            'city': 'Город',
            'housing_type': 'Тип жилья',
            'has_children': 'Есть дети',
            'has_other_pets': 'Есть другие животные',
            'experience_years': 'Опыт содержания животных',
            'activity_level': 'Ваш уровень активности',
            'time_at_home': 'Сколько времени вы проводите дома',
            'pet_preference': 'Какого питомца ищете',
            'pet_age_preference': 'Предпочтительный возраст питомца',
            'pet_gender_preference': 'Предпочтительный пол питомца',
            'adoption_goal': 'Цель усыновления',
            'ready_for_medical_care': 'Готов(а) ухаживать за питомцем с особенностями здоровья',
            'additional_info': 'Дополнительная информация',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Ваше ФИО'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Ваш возраст'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ваш город'}),
            'additional_info': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Если хотите, добавьте детали'}),
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label='Имя')
    email = forms.EmailField(label='Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин *'
        self.fields['username'].help_text = 'Используйте короткое имя для входа.'
        self.fields['first_name'].label = 'Имя *'
        self.fields['email'].label = 'Email *'
        self.fields['password1'].label = 'Пароль *'
        self.fields['password1'].help_text = 'Пароль должен быть достаточно надёжным.'
        self.fields['password2'].label = 'Повторите пароль *'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения.'

        self.fields['username'].widget.attrs.update({'placeholder': 'Ваш логин'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ваше имя'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ваш email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Придумайте пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.userprofile.role = 'user'
            user.userprofile.save()
        return user


class ShelterAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин *')
    password = forms.CharField(label='Пароль *', strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Ваш логин'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Ваш пароль'})


class AccountSettingsForm(forms.ModelForm):
    password1 = forms.CharField(
        required=False,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Новый пароль'}),
    )
    password2 = forms.CharField(
        required=False,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Логин',
            'email': 'Электронная почта',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ваш логин'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Добавьте почту'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get('class', '').strip()
            field.widget.attrs['class'] = f'{css_class} form-control'.strip()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', 'Пароли не совпадают.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class PetImportForm(forms.Form):
    file = forms.FileField(label='Excel-файл')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = self.fields['file'].widget.attrs.get('class', '').strip()
        self.fields['file'].widget.attrs['class'] = f'{css_class} form-control'.strip()
        self.fields['file'].widget.attrs['accept'] = '.xlsx'


class PetAdminForm(StyledModelForm):
    class Meta:
        model = Pet
        fields = [
            'name',
            'type',
            'gender',
            'age_months',
            'age_group',
            'description',
            'image',
            'sterilized',
            'vaccinated',
            'adopted',
            'can_live_with_children',
            'can_live_with_other_pets',
            'activity_level',
            'suitable_for_apartment',
            'requires_experience',
            'temperament',
            'health_status',
            'can_stay_alone',
        ]
        labels = {
            'name': 'Имя',
            'type': 'Вид',
            'gender': 'Пол',
            'age_months': 'Возраст в месяцах',
            'age_group': 'Возрастная группа',
            'description': 'История',
            'image': 'Фото',
            'sterilized': 'Стерилизован',
            'vaccinated': 'Привит',
            'adopted': 'Пристроен',
            'can_live_with_children': 'Можно в семью с детьми',
            'can_live_with_other_pets': 'Можно с другими животными',
            'activity_level': 'Уровень активности',
            'suitable_for_apartment': 'Подходит для квартиры',
            'requires_experience': 'Нужен опытный хозяин',
            'temperament': 'Характер',
            'health_status': 'Состояние здоровья',
            'can_stay_alone': 'Может оставаться один',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class NewsAdminForm(StyledModelForm):
    class Meta:
        model = News
        fields = ['title', 'summary', 'content', 'date', 'image']
        labels = {
            'title': 'Заголовок',
            'summary': 'Краткое описание',
            'content': 'Полный текст',
            'date': 'Дата публикации',
            'image': 'Изображение',
        }
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 8}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class AdoptionApplicationAdminForm(StyledModelForm):
    class Meta:
        model = AdoptionApplication
        fields = [
            'status',
            'admin_comment',
            'full_name',
            'email',
            'phone',
            'age',
            'city',
            'housing_type',
            'has_other_pets',
            'has_children',
            'experience',
            'why_adopt',
        ]
        labels = {
            'status': 'Статус',
            'admin_comment': 'Комментарий администратора',
            'full_name': 'ФИО',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'age': 'Возраст',
            'city': 'Город',
            'housing_type': 'Тип жилья',
            'has_other_pets': 'Есть другие животные',
            'has_children': 'Есть дети',
            'experience': 'Опыт содержания животных',
            'why_adopt': 'Почему хочет взять питомца',
        }
        widgets = {
            'admin_comment': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'why_adopt': forms.Textarea(attrs={'rows': 4}),
        }
