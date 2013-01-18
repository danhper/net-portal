from django.conf.urls import patterns, url

urlpatterns = patterns('course_navi.views',
    url(r'^$', 'index', name='index'),
    url(r'^timetable$', 'timetable', name='timetable'),
    url(r'^message$', 'message', name='message'),
    url(r'^news$', 'news', name='news'),
    url(r'^settings$', 'settings', name='settings'),
    url(r'^class$', 'lecture', name='lecture')
)
