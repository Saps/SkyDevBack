from django.urls import include, path
from rest_framework import routers
from .views import VacancyViewSet, VacancyReqViewSet, CandidateViewSet, EmpProfileViewSet, LoadListSet, StatParamSet, LoadRelSet

router = routers.DefaultRouter()

router.register(r'vacancies', VacancyViewSet)
router.register(r'vacanciesreq', VacancyReqViewSet)
router.register(r'candidate', CandidateViewSet)
router.register(r'empprofile', EmpProfileViewSet)
router.register(r'statparam', StatParamSet)

router.register(r'load', LoadListSet, basename='load')
router.register(r'loadrel', LoadRelSet, basename='loadrel')



urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]