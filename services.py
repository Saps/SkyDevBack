import os,time
from django.db.models import Q
import django
import agent_logic.helloworld as h

import agent_logic.parsing as pps
import agent_logic.similarity as smm


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skydev_drf.settings')
django.setup()

from skydev_app.models import Tasks, Vacancy, VacancyReq, Candidate, EmpProfile

print('Starting background services...')

while True:
    #time.sleep(5)
    res = Tasks.objects.filter(status='READY', blocked=0).first()
    if res:
        #res.blocked = 1
        #res.save()

        # стоп сервиса
        if res.name == 'quit':
            break
        # сервис-заглушка
        if res.name == 'hello':
            outp = h.run(res.in_params)
            res.out_params = outp
            res.blocked = 0
            res.status='COMPLETED'
            res.save()
            continue
        # сервис парсинга резюме
        if res.name == 'parsing':
            if 'vacancy_id' in res.in_params:
                vac = Vacancy.objects.filter(id = res.in_params['vacancy_id']).first()
                if vac:
                    pars_inparams = {
                        'keywords': vac.keywords,
                        'query': vac.name,
                    }
                    outp = pps.run(pars_inparams)
                    for outc in outp:
                        u_fio = outc['hyperlink'].replace('/resume/','')
                        cdd = Candidate.objects.filter(fio = u_fio).count()
                        if cdd > 0:
                            continue
                        c = Candidate(
                            fio = u_fio,
                            hyperlink = outc['hyperlink'],
                            rawtext = outc['rawtext']
                        )
                        c.save()
                        ep = EmpProfile(
                            candidate_id = c.id,
                            vacancy_id = vac.id,
                            rawtext = outc['rawtext']
                        )
                        ep.save()
                    res.out_params = {'result' : f'Отработало нормально, нашло {len(outp)} кандидатов'}
                else:
                    res.out_params = {'result': f"Не найдена вакансия с id={res.in_params['vacancy_id']}"}
            else:
                res.out_params = {'result' : 'Не задан Vacancy_id'}
            res.blocked = 0
            res.status='COMPLETED'
            res.save()
            continue

        if res.name == 'similarity':
            if 'vacancy_id' in res.in_params:
                vac = Vacancy.objects.filter(id = res.in_params['vacancy_id']).first()
                if vac:
                    text_vac = ''
                    vac_req = VacancyReq.objects.filter(vacancy_id=vac.id).all()
                    for curr_vr in vac_req:
                        text_vac += " " + curr_vr.duties
                        text_vac += " " + curr_vr.requirements
                    # перебираем резюме
                    epf = EmpProfile.objects.filter(vacancy_id=vac.id).all()
                    for curr_ep in epf:
                        resc = smm.run(
                            {
                                "vacancy_txt": text_vac,
                                "resume_txt": curr_ep.rawtext
                            }
                        )
                        curr_ep.similarity_score = resc['detail']['similarity_score']
                        curr_ep.save()
                    res.out_params = {'result': f'Отработало нормально, апдейтило {len(epf)} записей'}
                else:
                    res.out_params = {'result': f"Не найдена вакансия с id={res.in_params['vacancy_id']}"}
            else:
                res.out_params = {'result' : 'Не задан Vacancy_id'}
            res.blocked = 0
            res.status='COMPLETED'
            res.save()
            continue

    else:
        time.sleep(1)

print('Background services down')