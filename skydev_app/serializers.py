from rest_framework import serializers
from .models import Vacancy, VacancyReq, Candidate, EmpProfile



class VacancySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = Vacancy
        fields = ('id', 'name', 'status', 'region', 'town', 'address')


class VacancyReqSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = VacancyReq
        fields = ('id', 'vacancy', 'whois', 'duties', 'requirements')


class CandidateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = Candidate
        fields = ('id', 'fio', 'region', 'town', 'contacts', 'status', 'foreign_langs')



class EmpProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Domain"""

    class Meta:
        model = EmpProfile
        fields = ('candidate', 'specs', 'contract_type', 'emp_type', 'work_sced',
                  'software_knowledges', 'software_skills', 'allow_trip')

