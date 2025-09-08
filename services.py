import os,time
from django.db.models import Q
import django
import agent_logic.helloworld as h

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skydev_drf.settings')
django.setup()

from skydev_app.models import Tasks

print('Starting background services...')

while True:
    #time.sleep(5)
    res = Tasks.objects.filter(status='READY', blocked=0).first()
    if res:
        res.blocked = 1
        res.save()
        if res.name == 'quit':
            break
        if res.name == 'hello':
            outp = h.run(res.in_params)
            res.out_params = outp
            res.blocked = 0
            res.status='COMPLETED'
            res.save()
            continue
    else:
        time.sleep(1)

print('Background services down')