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
class LoadViewSet(viewsets.ViewSet):
    #list(), create(), retrieve(), update(), partial_update(), destroy().
    def list(self, request):
        return Response('Hello list')

