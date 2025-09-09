# Create your views here.
from django.contrib.admin.templatetags.admin_list import result_list
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vacancy, VacancyReq, Candidate, EmpProfile, Tasks, StatParams
from .serializers import VacancySerializer, VacancyReqSerializer, CandidateSerializer, EmpProfileSerializer, StatParamSerializer


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
        # вывод листа вакансий
        resultat = []
        res = Vacancy.objects.filter(status=1).all()

        for curr_res in res:
            curr_struct = {"id" : curr_res.id,
             "name" : curr_res.name,
             "region" : curr_res.region,
             "contract_type" : curr_res.contract_type,
             "income" : curr_res.income,
             "software_knowledges" : curr_res.software_knowledges,
             "software_skills" : curr_res.software_skills,
             "duties" : "",
             "requirements": ""}
            vac_req = VacancyReq.objects.filter(vacancy_id = curr_res.id).all()
            for curr_vr in vac_req:
                curr_struct["duties"] += ", " + curr_vr.duties
                curr_struct["requirements"] += ", " + curr_vr.requirements
            resultat.append(curr_struct)

        return Response(data = resultat, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        resultat = []
        emps = EmpProfile.objects.filter(vacancy_id=pk).all()

        resp = []
        for cur_emp in emps:
            single_emp = Candidate.objects.filter(id = cur_emp.candidate_id).first()

            another_rec = {"id": cur_emp.id,
                 "fio": single_emp.fio,
                 "town": single_emp.town,
                 "compliance": cur_emp.similarity_score * 100,
                 "complete": 20,
                 "reliability": 60}

            resp.append(another_rec)

        # вывод листа кандидатов (ранжированный с )
        return Response(data = resp, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        in_par = {'vacancy_id' : pk}
        tsk = Tasks(
            name = 'parsing',
            status = 'READY',
            blocked = 0,
            in_params = in_par,
            out_params = {}
        )
        tsk.save()
        data = {
            "result" : "Отправлен на формирование",
            "vacancy_id" : pk
        }
        return Response(data = data, status=status.HTTP_200_OK)

    #@action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        if pk:
            return Response(data={f'Отправлены задания кандидату {pk}'}, status=status.HTTP_200_OK)
        else:
            return Response(data={"Не задан кандидат"}, status=status.HTTP_200_OK)


class LoadRelSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def update(self, request, pk=None):
        in_par = {'vacancy_id': pk}
        tsk = Tasks(
            name='similarity',
            status='READY',
            blocked=0,
            in_params=in_par,
            out_params={}
        )
        tsk.save()
        data = {
            "result": "Отправлен на формирование",
            "vacancy_id": pk
        }
        return Response(data=data, status=status.HTTP_200_OK)


class StatParamSet(viewsets.ModelViewSet):
    queryset = StatParams.objects.all()
    serializer_class = StatParamSerializer
    permission_classes = [permissions.AllowAny]
