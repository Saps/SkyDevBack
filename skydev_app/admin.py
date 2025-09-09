from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.
from .models import Vacancy, Candidate, EmpProfile, VacancyReq

#admin.site.register(Project)
admin.site.site_header = "Администрирование БД системы"

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ['name']


admin.site.register(Vacancy,VacancyAdmin)

class VacancyReqAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'whois', 'duties', 'requirements')
    list_display_links = ['whois']

admin.site.register(VacancyReq,VacancyReqAdmin)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'status', 'photo')
    list_display_links = ['fio']

admin.site.register(Candidate, CandidateAdmin)


class EmpProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'cand_name', 'specs')
    list_display_links = ['cand_name']

    list_select_related = ['candidate']  # To avoid extra queries

    def cand_name(self, emp_profile):
        return emp_profile.candidate.fio


admin.site.register(EmpProfile, EmpProfileAdmin)
