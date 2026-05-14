from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('volunteer', 'Волонтёр'),
        ('admin', 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f'{self.user.username} ({self.role})'


class Pet(models.Model):
    TYPE_CHOICES = [
        ('cat', 'Кошка'),
        ('dog', 'Собака'),
    ]

    GENDER_CHOICES = [
        ('male', 'Мальчик'),
        ('female', 'Девочка'),
    ]

    ACTIVITY_CHOICES = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ]

    AGE_GROUP_CHOICES = [
        ('young', 'Молодой'),
        ('adult', 'Взрослый'),
    ]

    TEMPERAMENT_CHOICES = [
        ('calm', 'Спокойный'),
        ('active', 'Активный'),
        ('friendly', 'Дружелюбный'),
        ('careful', 'Осторожный'),
    ]

    HEALTH_STATUS_CHOICES = [
        ('healthy', 'Здоров'),
        ('care_needed', 'Нужен особый уход'),
    ]

    name = models.CharField('Имя', max_length=100)
    type = models.CharField('Вид', max_length=10, choices=TYPE_CHOICES)
    gender = models.CharField('Пол', max_length=6, choices=GENDER_CHOICES)
    age_months = models.PositiveIntegerField('Возраст в месяцах', default=0)
    description = models.TextField('История', blank=True)
    image = models.ImageField('Фото', upload_to='pet_photos/', blank=True, null=True)
    sterilized = models.BooleanField('Стерилизован', default=False)
    vaccinated = models.BooleanField('Привит', default=False)
    adopted = models.BooleanField('Пристроен', default=False)

    can_live_with_children = models.BooleanField('Можно в семью с детьми', default=True)
    can_live_with_other_pets = models.BooleanField('Можно с другими животными', default=True)
    activity_level = models.CharField('Уровень активности', max_length=20, choices=ACTIVITY_CHOICES, default='medium')
    suitable_for_apartment = models.BooleanField('Подходит для квартиры', default=True)
    requires_experience = models.BooleanField('Требуется опытный хозяин', default=False)

    age_group = models.CharField(
        'Возрастная группа',
        max_length=10,
        choices=AGE_GROUP_CHOICES,
        default='adult',
    )
    temperament = models.CharField(
        'Характер',
        max_length=20,
        choices=TEMPERAMENT_CHOICES,
        default='friendly',
    )
    health_status = models.CharField(
        'Состояние здоровья',
        max_length=20,
        choices=HEALTH_STATUS_CHOICES,
        default='healthy',
    )
    can_stay_alone = models.BooleanField('Может оставаться один', default=True)

    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'

    def age_display(self):
        years = self.age_months // 12
        months = self.age_months % 12

        parts = []
        if years > 0:
            parts.append(f'{years} {self.pluralize_years(years)}')
        if months > 0:
            parts.append(f'{months} {self.pluralize_months(months)}')
        if not parts:
            return '0 месяцев'
        return ' '.join(parts)

    @staticmethod
    def pluralize_years(number):
        if 11 <= number % 100 <= 14:
            return 'лет'
        if number % 10 == 1:
            return 'год'
        if 2 <= number % 10 <= 4:
            return 'года'
        return 'лет'

    @staticmethod
    def pluralize_months(number):
        if 11 <= number % 100 <= 14:
            return 'месяцев'
        if number % 10 == 1:
            return 'месяц'
        if 2 <= number % 10 <= 4:
            return 'месяца'
        return 'месяцев'


class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('review', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('meeting', 'Назначено знакомство'),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Питомец',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='adoption_applications',
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )

    full_name = models.CharField('ФИО', max_length=150)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=30)
    age = models.PositiveIntegerField('Возраст')
    city = models.CharField('Город', max_length=100)
    housing_type = models.CharField('Тип жилья', max_length=100)
    has_other_pets = models.BooleanField('Есть другие животные', default=False)
    has_children = models.BooleanField('Есть дети', default=False)
    experience = models.TextField('Опыт содержания животных', blank=True)
    why_adopt = models.TextField('Почему хотите взять животное')
    created_at = models.DateTimeField('Дата подачи', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    admin_comment = models.TextField('Комментарий администратора', blank=True)

    class Meta:
        verbose_name = 'Заявка на усыновление'
        verbose_name_plural = 'Заявки на усыновление'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка от {self.full_name} на {self.pet.name}'


class OwnerQuestionnaire(models.Model):
    HOUSING_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Частный дом'),
        ('rented', 'Съёмное жильё'),
    ]

    ACTIVITY_CHOICES = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ]

    PET_PREFERENCE_CHOICES = [
        ('cat', 'Кошка'),
        ('dog', 'Собака'),
        ('any', 'Не важно'),
    ]

    TIME_AT_HOME_CHOICES = [
        ('rarely', 'Редко бываю дома'),
        ('often', 'Часто бываю дома'),
        ('always', 'Почти всегда дома'),
    ]

    PET_AGE_PREFERENCE_CHOICES = [
        ('young', 'Молодой'),
        ('adult', 'Взрослый'),
        ('any', 'Не важно'),
    ]

    PET_GENDER_PREFERENCE_CHOICES = [
        ('male', 'Мальчик'),
        ('female', 'Девочка'),
        ('any', 'Не важно'),
    ]

    ADOPTION_GOAL_CHOICES = [
        ('companion', 'Компаньон'),
        ('family', 'Для семьи'),
        ('active_walks', 'Для активных прогулок'),
        ('any', 'Не важно'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='owner_questionnaires',
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )
    full_name = models.CharField('ФИО', max_length=150)
    age = models.PositiveIntegerField('Возраст')
    city = models.CharField('Город', max_length=100)
    housing_type = models.CharField('Тип жилья', max_length=20, choices=HOUSING_CHOICES)
    has_children = models.BooleanField('Есть дети', default=False)
    has_other_pets = models.BooleanField('Есть другие животные', default=False)
    experience_years = models.PositiveIntegerField('Опыт содержания животных (лет)', default=0)
    activity_level = models.CharField('Уровень активности', max_length=20, choices=ACTIVITY_CHOICES)
    time_at_home = models.CharField('Сколько времени проводите дома', max_length=20, choices=TIME_AT_HOME_CHOICES)
    pet_preference = models.CharField(
        'Предпочтение по типу животного',
        max_length=10,
        choices=PET_PREFERENCE_CHOICES,
        default='any',
    )
    pet_age_preference = models.CharField(
        'Предпочтительный возраст питомца',
        max_length=10,
        choices=PET_AGE_PREFERENCE_CHOICES,
        default='any',
    )
    pet_gender_preference = models.CharField(
        'Предпочтительный пол питомца',
        max_length=10,
        choices=PET_GENDER_PREFERENCE_CHOICES,
        default='any',
    )
    adoption_goal = models.CharField(
        'Цель усыновления',
        max_length=20,
        choices=ADOPTION_GOAL_CHOICES,
        default='any',
    )
    ready_for_medical_care = models.BooleanField(
        'Готов(а) ухаживать за питомцем с особенностями здоровья',
        default=False,
    )
    additional_info = models.TextField('Дополнительная информация', blank=True)
    created_at = models.DateTimeField('Дата заполнения', auto_now_add=True)

    class Meta:
        verbose_name = 'Анкета будущего хозяина'
        verbose_name_plural = 'Анкеты будущих хозяев'
        ordering = ['-created_at']

    def __str__(self):
        return f'Анкета: {self.full_name}'


class Feedback(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение')
    submitted_at = models.DateTimeField('Дата отправки', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} ({self.email})'


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Полный текст')
    date = models.DateField(verbose_name='Дата публикации')
    image = models.ImageField(
        upload_to='news_images/',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']

    def __str__(self):
        return self.title
