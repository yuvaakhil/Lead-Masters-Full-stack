from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Exam(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.IntegerField(default=5)
    total_questions = models.IntegerField(default=10)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exam.title} - Q{self.id}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Q{self.question.id} - {self.choice_text[:40]}{' ✔' if self.is_correct else ''}"


class ExamSession(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_sessions')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sessions')
    attempt_number = models.IntegerField(default=1)  # ✅ New field
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)

    class Meta:
        constraints = [
                   models.UniqueConstraint(fields=['user', 'exam', 'attempt_number'], name='unique_user_exam_attempt')

        ]

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} ({self.status})"

    def calculate_score(self):
        """Recalculate score based on StudentAnswers."""
        answers = self.answers.all()
        correct = sum(1 for ans in answers if ans.selected_choice and ans.selected_choice.is_correct)
        self.correct_answers = correct
        self.score = (correct / self.total_questions) * 100 if self.total_questions > 0 else 0
        self.save()


class StudentAnswer(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True, related_name='chosen_answers')
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'question'], name='unique_session_question_answer')
        ]

    def __str__(self):
        return f"{self.session.user.username} - {self.question.id} -> {self.selected_choice}"
