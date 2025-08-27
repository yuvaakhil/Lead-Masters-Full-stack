from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
import random
from .models import Exam, Question, ExamSession, StudentAnswer, Choice
from .serializers import (
    ExamSerializer, QuestionSerializer, ExamSessionSerializer,
    StudentAnswerSerializer, ExamResultSerializer
)

@api_view(['GET'])
def available_exams(request):
    """Get list of available exams"""
    exams = Exam.objects.filter(is_active=True)
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def start_exam(request, exam_id):
    """Start a new exam session (with attempts)"""
    exam = get_object_or_404(Exam, id=exam_id, is_active=True)

    # ✅ Count past attempts for this user on this exam
    attempt_count = ExamSession.objects.filter(user=request.user, exam=exam).count()

    # ✅ Create a new session with attempt_number = previous + 1
    session = ExamSession.objects.create(
        user=request.user,
        exam=exam,
        attempt_number=attempt_count + 1,
        total_questions=exam.total_questions
    )

    serializer = ExamSessionSerializer(session)
    return Response({
        'message': f'Exam session started successfully (Attempt #{session.attempt_number})',
        'session': serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_exam_questions(request, session_id):
    """Get randomized questions for exam session"""
    session = get_object_or_404(ExamSession, session_id=session_id, user=request.user)

    if session.status != 'in_progress':
        return Response({'error': 'This exam session is not active'}, status=status.HTTP_400_BAD_REQUEST)

    # Expiry check
    duration = timedelta(minutes=session.exam.duration_minutes)
    if timezone.now() > session.start_time + duration:
        session.status = 'expired'
        session.end_time = timezone.now()
        session.save()
        return Response({'error': 'Exam session has expired'}, status=status.HTTP_400_BAD_REQUEST)

    # Random question selection
    all_questions = list(session.exam.questions.all())
    selected_questions = random.sample(all_questions, min(session.exam.total_questions, len(all_questions)))

    serializer = QuestionSerializer(selected_questions, many=True)
    return Response({
        'session_id': session.session_id,
        'questions': serializer.data,
        'duration_minutes': session.exam.duration_minutes,
        'start_time': session.start_time
    })

@api_view(['POST'])
def submit_answer(request, session_id):
    """Submit answer for a question"""
    session = get_object_or_404(ExamSession, session_id=session_id, user=request.user)

    if session.status != 'in_progress':
        return Response({'error': 'This exam session is not active'}, status=status.HTTP_400_BAD_REQUEST)

    question_id = request.data.get('question_id')
    choice_id = request.data.get('choice_id')

    if not question_id:
        return Response({'error': 'Question ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    question = get_object_or_404(Question, id=question_id, exam=session.exam)
    choice = None

    if choice_id:
        choice = get_object_or_404(Choice, id=choice_id, question=question)

    # Save or update answer
    StudentAnswer.objects.update_or_create(
        session=session,
        question=question,
        defaults={'selected_choice': choice}
    )

    return Response({'message': 'Answer submitted successfully', 'question_id': question_id, 'choice_id': choice_id})

@api_view(['POST'])
def submit_exam(request, session_id):
    """Submit the complete exam and calculate score"""
    session = get_object_or_404(ExamSession, session_id=session_id, user=request.user)

    if session.status != 'in_progress':
        return Response({'error': 'This exam session is not active'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        correct_answers = sum(
            1 for answer in session.answers.all()
            if answer.selected_choice and answer.selected_choice.is_correct
        )
        total_answered = session.answers.count()
        score = (correct_answers / total_answered) * 100 if total_answered > 0 else 0

        session.status = 'completed'
        session.end_time = timezone.now()
        session.score = score
        session.correct_answers = correct_answers
        session.save()

    serializer = ExamResultSerializer(session)
    return Response({'message': 'Exam submitted successfully', 'result': serializer.data})

@api_view(['GET'])
def get_exam_result(request, session_id):
    """Get exam result"""
    session = get_object_or_404(
        ExamSession, session_id=session_id, user=request.user, status='completed'
    )
    serializer = ExamResultSerializer(session)
    return Response(serializer.data)

@api_view(['GET'])
def user_exam_history(request):
    """Get user's exam history"""
    sessions = ExamSession.objects.filter(user=request.user, status='completed').order_by('-end_time')
    serializer = ExamResultSerializer(sessions, many=True)
    return Response(serializer.data)
