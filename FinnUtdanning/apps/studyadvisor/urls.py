from django.conf.urls import url

from apps.studyadvisor.views import frontpage, prev_searches, nyInteresse, nyttStudie, endre, endreInteresse, endreStudie, slettInteresse, slettStudie, personligFargetema, globaltFargetema

urlpatterns = [
    url(r'^forslag/$', frontpage, name='studieforslag'),
    url(r'^tidligere_søk/$', prev_searches, name='tidligere_sok'),
    url(r'^nyInteresse/$', nyInteresse, name='nyInteresse'),
    url(r'^nyttStudie/$', nyttStudie, name='nyttStudie'),
    url(r'^endre/$', endre, name='endre'),
    url(r'^endre/interesse/(?P<id>\d+)/$', endreInteresse, name='endreInteresse'),
    url(r'^endre/studie/(?P<id>\d+)/$', endreStudie, name='endreStudie'),
    url(r'^endre/interesse/slett/(?P<id>\d+)/$', slettInteresse, name='slettInteresse'),
    url(r'^endre/studie/slett/(?P<id>\d+)/$', slettStudie, name='slettStudie'),
    url(r'^personligFargetema/$', personligFargetema, name='personligFargetema'),
    url(r'^globaltFargetema/$', globaltFargetema, name='globaltFargetema'),
]
