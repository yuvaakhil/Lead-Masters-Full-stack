from rest_framework import serializers
from .models import Exam, Question, Choice, ExamSession, StudentAnswer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'choices')

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('id', 'title', 'description', 'duration_minutes', 'total_questions', 'difficulty')

class ExamSessionSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    
    class Meta:
        model = ExamSession
        fields = ('session_id', 'exam', 'start_time', 'status', 'score', 'total_questions', 'correct_answers')

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ('question', 'selected_choice')

class ExamResultSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    
    class Meta:
        model = ExamSession
        fields = ('session_id', 'exam', 'start_time', 'end_time', 'score', 'total_questions', 'correct_answers', 'status')