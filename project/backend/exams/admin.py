from django.contrib import admin
from .models import Exam, Question, Choice, ExamSession, StudentAnswer

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration_minutes', 'total_questions', 'is_active', 'created_at')
    list_filter = ('difficulty', 'is_active', 'created_at')
    search_fields = ('title', 'description')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_text', 'difficulty', 'created_at')
    list_filter = ('exam', 'difficulty', 'created_at')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'status', 'score', 'start_time', 'end_time')
    list_filter = ('status', 'exam', 'start_time')
    search_fields = ('user__email', 'exam__title')
    readonly_fields = ('session_id', 'start_time')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'selected_choice', 'answered_at')
    list_filter = ('session__exam', 'answered_at')
    search_fields = ('session__user__email',)