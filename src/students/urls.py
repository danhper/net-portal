from django.conf.urls import patterns, url

urlpatterns = patterns('students.views',
    url(r'^login$', 'login', name='login'),
    url(r'^make_login$', 'make_login', name='make_login'),
)
