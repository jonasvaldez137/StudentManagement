from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Student, Subject, Enrollment, Grade
from .serializers import (
    StudentSerializer, SubjectSerializer,
    EnrollmentSerializer, GradeSerializer,
    StudentDetailSerializer
)

class IndexPageView(TemplateView):
    template_name = 'app/index.html'

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['get'])
    def detail_with_enrollments(self, request, pk=None):
        student = self.get_object()
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student).select_related('subject')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().select_related('student', 'subject')
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id', None)
        if student_id is not None:
            queryset = queryset.filter(student_id=student_id)
        return queryset


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all().select_related('enrollment__student', 'enrollment__subject')
    serializer_class = GradeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        enrollment_id = self.request.query_params.get('enrollment_id', None)
        student_id = self.request.query_params.get('student_id', None)

        if enrollment_id is not None:
            queryset = queryset.filter(enrollment_id=enrollment_id)
        elif student_id is not None:
            queryset = queryset.filter(enrollment__student_id=student_id)

        return queryset


def index(request):
    return render(request, 'base.html')