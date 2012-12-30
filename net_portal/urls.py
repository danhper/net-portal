from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'course_navi.views.index', name='index'),
    url(r'^timetable$', 'course_navi.views.timetable', name='timetable'),
    url(r'^message$', 'course_navi.views.message', name='message'),
    url(r'^news$', 'course_navi.views.news', name='news'),
    url(r'^settings$', 'course_navi.views.settings', name='settings'),
    url(r'^class$', 'course_navi.views.lecture', name='lecture'),
    url(r'^login$', 'students.views.login', name='login'),
)
