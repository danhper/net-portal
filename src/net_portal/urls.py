from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='index'),
    url(r'^', include('students.urls')),
    url(r'^cnavi/', include('course_navi.urls', namespace='cnavi', app_name='cnavi'))
)
