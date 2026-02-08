from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('experience', 'predicted_salary', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('experience',)
