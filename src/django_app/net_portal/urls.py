from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='index'),
    url(r'^', include('students.urls', namespace='students', app_name='students')),
    url(r'^cnavi/', include('course_navi.urls', namespace='cnavi', app_name='cnavi')),
    url(r'^about$', 'portal.views.about', name='about'),
    url(r'^team$', 'portal.views.team', name='team'),
    url(r'^contact$', 'portal.views.contact', name='contact')
)
