from django.conf.urls import patterns, url, include
from students.views import *


registration_patterns = patterns('',
    url(r'^registration/update$', update, name='registration_update')
)

session_patterns = patterns('',
    url(r'^login$', login, name='login'),
    url(r'^make_login$', make_login, name='make_login'),
    url(r'^logout$', logout, name='logout')
)

urlpatterns = patterns('students.views',
    url(r'^cnavi/', include(registration_patterns)),
    url(r'^', include(session_patterns))
)
