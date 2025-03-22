from django.contrib import admin
from .models import InterviewResponse  # Import the model

@admin.register(InterviewResponse)
class InterviewResponseAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'question', 'score', 'feedback', 'created_at')  # Customize fields
    search_fields = ('candidate__name', 'question', 'answer')  # Add search functionality
    list_filter = ('score',)  # Add filter by score

# OR simply register without customization:
# admin.site.register(InterviewResponse)

