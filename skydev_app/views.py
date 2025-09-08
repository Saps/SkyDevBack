# Create your views here.
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vacancy, VacancyReq, Candidate, EmpProfile
from .serializers import VacancySerializer, VacancyReqSerializer, CandidateSerializer, EmpProfileSerializer


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class VacancyReqViewSet(viewsets.ModelViewSet):
    queryset = VacancyReq.objects.all()
    serializer_class = VacancyReqSerializer
    permission_classes = [permissions.AllowAny]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]


class EmpProfileViewSet(viewsets.ModelViewSet):
    queryset = EmpProfile.objects.all()
    serializer_class = EmpProfileSerializer
    permission_classes = [permissions.AllowAny]

#--------------------------------------------------------------
class LoadListSet(viewsets.ViewSet):
    #list(), create(), retrieve(), update(), partial_update(), destroy().
    def list(self, request):
        # вывод листа кандидатов (ранжированный с )
        return Response('List of open vacancies')

    def retrieve(self, request, pk=None):
        # вывод листа кандидатов (ранжированный с )
        return Response('List of candidates to vacancy')

    def create(self, request):
        return Response('Form or update list of candidates')

    def update(self, request, pk=None):
        return Response('Set Services to Candidate')