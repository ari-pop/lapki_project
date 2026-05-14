from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import AdoptionApplication, Feedback, News, OwnerQuestionnaire, Pet


class ShelterPagesTests(TestCase):
    def setUp(self):
        self.pet = Pet.objects.create(
            name='Барсик',
            type='cat',
            gender='male',
            age_months=24,
            description='Спокойный и ласковый кот.',
            vaccinated=True,
            sterilized=True,
        )
        self.news = News.objects.create(
            title='Открыли новый вольер',
            summary='Короткая новость о жизни приюта.',
            content='Подробности о новом вольере для животных.',
            date='2026-04-21',
        )

    def test_main_pages_are_available(self):
        page_names = [
            'home',
            'about',
            'help',
            'contacts',
            'pets',
            'news',
            'owner_questionnaire',
            'account_home',
            'login',
            'register',
        ]

        for page_name in page_names:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 200)

    def test_news_detail_page_is_available(self):
        response = self.client.get(reverse('news_detail', args=[self.news.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)

    def test_register_creates_user_and_profile_role(self):
        response = self.client.post(
            reverse('register'),
            data={
                'username': 'maria',
                'first_name': 'Мария',
                'email': 'maria@example.com',
                'password1': 'SaitStrongPass123',
                'password2': 'SaitStrongPass123',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='maria')
        self.assertEqual(user.userprofile.role, 'user')
        self.assertContains(response, 'Личный кабинет')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_owner_questionnaire_is_saved_for_logged_user(self):
        user = User.objects.create_user(
            username='ivan',
            password='SaitStrongPass123',
            first_name='Иван',
            email='ivan@example.com',
        )
        self.client.login(username='ivan', password='SaitStrongPass123')

        response = self.client.post(
            reverse('owner_questionnaire'),
            data={
                'full_name': 'Иван Иванов',
                'age': 30,
                'city': 'Таганрог',
                'housing_type': 'apartment',
                'has_children': 'False',
                'has_other_pets': 'False',
                'has_pet_experience': 'True',
                'experience_years': 1,
                'activity_level': 'medium',
                'time_at_home': 'often',
                'pet_preference': 'cat',
                'pet_age_preference': 'adult',
                'pet_gender_preference': 'male',
                'adoption_goal': 'companion',
                'ready_for_medical_care': False,
                'additional_info': 'Нужен спокойный домашний питомец.',
            },
        )

        self.assertEqual(response.status_code, 200)
        questionnaire = OwnerQuestionnaire.objects.get()
        self.assertEqual(questionnaire.user, user)
        self.assertEqual(questionnaire.experience_years, 1)
        self.assertContains(response, self.pet.name)

    def test_adoption_application_is_saved_for_logged_user(self):
        user = User.objects.create_user(
            username='anna',
            password='SaitStrongPass123',
            first_name='Анна',
            email='anna@example.com',
        )
        self.client.login(username='anna', password='SaitStrongPass123')

        response = self.client.post(
            reverse('adoption_application', args=[self.pet.pk]),
            data={
                'full_name': 'Анна Смирнова',
                'email': 'anna@example.com',
                'phone': '+79990000000',
                'age': 28,
                'city': 'Таганрог',
                'housing_type': 'Квартира',
                'has_other_pets': False,
                'has_children': False,
                'experience': 'Есть опыт.',
                'why_adopt': 'Хочу забрать питомца домой.',
            },
        )

        self.assertEqual(response.status_code, 302)
        application = AdoptionApplication.objects.get()
        self.assertEqual(application.user, user)

    def test_feedback_form_creates_record(self):
        response = self.client.post(
            reverse('help'),
            data={
                'name': 'Анна',
                'email': 'anna@example.com',
                'message': 'Хочу помочь приюту кормом.',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertContains(response, 'Сообщение отправлено!')
