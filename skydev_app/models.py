from django.db import models
from .choices import *

# Create your models here.

class Vacancy(models.Model):
    status = models.IntegerField(choices=VACANCY_STATUSES, null=True)
    name = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    contract_type = models.IntegerField(choices=CONTRACT_STATUSES, null=True)
    emp_type = models.IntegerField(choices=EMP_STATUSES, null=True)
    work_sced = models.IntegerField(choices=WS_STATUSES, null=True)
    income = models.IntegerField(null=True)
    salary_max = models.IntegerField(null=True)
    salary_min = models.IntegerField(null=True)
    ann_premium = models.IntegerField(null=True)
    premium_type = models.IntegerField(choices=PREMIUM_TYPE_STATUSES,null=True)
    edu_level = models.IntegerField(choices=EDU_LEVEL_STATUSES,null=True)
    experience = models.IntegerField(null=True)
    software_knowledges = models.CharField(max_length=255,null=True)
    software_skills = models.CharField(max_length=255,null=True)
    foreign_langs = models.CharField(max_length=255,null=True)
    allow_trip = models.IntegerField(choices=AT_STATUSES,null=True)
    change_date = models.DateTimeField(null=True)
    keywords = models.TextField(null=True)


class VacancyReq(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    whois = models.CharField(max_length=255, null=True)
    duties = models.TextField()
    requirements = models.TextField()


class Candidate(models.Model):
    fio = models.CharField(max_length=255,null=True)
    region = models.CharField(max_length=255,null=True)
    town = models.CharField(max_length=255,null=True)
    contacts = models.TextField(null=True)
    status = models.IntegerField(choices=AVA_STATUSES,null=True)
    photo = models.ImageField()
    foreign_langs = models.CharField(max_length=255,null=True)
    hyperlink = models.TextField(null=True)
    rawtext = models.TextField(null=True)


class EmpProfile(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE,null=True)
    specs = models.TextField(null=True)
    contract_type = models.IntegerField(choices=CONTRACT_STATUSES,null=True)
    emp_type = models.IntegerField(choices=EMP_STATUSES,null=True)
    work_sced = models.IntegerField(choices=WS_STATUSES,null=True)
    software_knowledges = models.CharField(max_length=255,null=True)
    software_skills = models.CharField(max_length=255,null=True)
    allow_trip = models.IntegerField(choices=AT_STATUSES,null=True)
    rawtext = models.TextField(null=True)
    similarity_score = models.FloatField(null=True, default=0)


class Tasks(models.Model):
    name = models.TextField()
    status = models.CharField(max_length=255)
    blocked = models.BooleanField(default=False)
    in_params = models.JSONField()
    out_params = models.JSONField()


class StatParams(models.Model):
    name = models.TextField()
    caption = models.TextField()
    value = models.FloatField()
    ordernum = models.IntegerField()