# Create your views here.
from django.contrib.admin.templatetags.admin_list import result_list
from rest_framework import viewsets, permissions, filters, status
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
    permission_classes = [permissions.AllowAny]
    #list(), create(), retrieve(), update(), partial_update(), destroy().
    def list(self, request):
        # вывод листа кандидатов (ранжированный с )
        resultat = [
            {"id" : '1',
             "name" : "Курьер",
             "region" : "Москва",
             "contract_type" : "1",
             "income" : "20000",
             "software_knowledges" : "DBeaves, MySQLAdmin, PHPStorm, алгоритмы",
             "software_skills" : "PHP SQL HTTP REST",
             "duties" : "Доставлять заказы в удобном для тебя районе: у Ozon fresh большое количество локаций—выберу ту, которая ближе к дому",
             "requirements": "Сможешь использовать для заказов свой телефон на Android"},
            {"id" : '5',
             "name" : "Велокурьер ",
             "region" : "Москва",
             "contract_type" : "1",
             "income" : "20000",
             "software_knowledges" : "DBeaves, MySQLAdmin, PHPStorm, алгоритмы",
             "software_skills" : "PHP SQL HTTP REST",
             "duties" : "Никакой еды, пиццы, никакого шашлыка, никаких кирпичей. Только лёгкие посылки",
             "requirements": "Немного желания двигаться и зарабатывать"}
        ]
        return Response(data = resultat, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        resp = []
        if pk == '1':
            resp = [
                {"id" : "6",
                 "fio" : "Иванов Петр Иванович",
                 "town" : "Москва",
                 "compliance" : 80,
                 "complete" : 20,
                 "reliability" : 60},
                {"id" : "8",
                 "fio": "Сидоров Петр Иванович",
                 "town": "Москва",
                 "compliance": 70,
                 "complete": 60,
                 "reliability": 30}
            ]
        if pk == '5':
            resp = [
                {"id" : "3",
                 "fio" : "Петруччо",
                 "town" : "Москва",
                 "compliance" : 80,
                 "complete" : 20,
                 "reliability" : 60},
                {"id" : "4",
                 "fio": "Чиполино",
                 "town": "Москва",
                 "compliance": 70,
                 "complete": 60,
                 "reliability": 30}
            ]

        # вывод листа кандидатов (ранжированный с )
        return Response(data = resp, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        data = {
            "result" : "Отправлен на формирование",
            "id vaca" : pk
        }
        return Response(data = data, status=status.HTTP_200_OK)

    #@action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        if pk:
            return Response(data={f'Отправлены задания кандидату {pk}'}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Не задан кандидат"}, status=status.HTTP_200_OK)