from django.contrib import admin
from .models import UserProfile
from .models import Pet, Feedback, News, AdoptionApplication, OwnerQuestionnaire

@admin.register(OwnerQuestionnaire)
class OwnerQuestionnaireAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'user', 'city', 'housing_type',
        'activity_level', 'pet_preference',
        'pet_age_preference', 'created_at'
    )
    list_filter = (
        'housing_type', 'activity_level', 'pet_preference',
        'pet_age_preference', 'pet_gender_preference',
        'adoption_goal', 'ready_for_medical_care', 'created_at'
    )
    search_fields = ('full_name', 'city')
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'gender', 'age_months',
        'activity_level', 'age_group', 'health_status',
        'requires_experience', 'adopted'
    )
    list_filter = (
        'type', 'gender', 'adopted',
        'can_live_with_children', 'can_live_with_other_pets',
        'activity_level', 'age_group', 'health_status',
        'suitable_for_apartment', 'requires_experience', 'can_stay_alone'
    )
    search_fields = ('name', 'description')

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'pet', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'pet')
    search_fields = ('full_name', 'email', 'phone', 'pet__name')
    

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email', 'message')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title', 'content')
