from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'course_navi.views.index', name='index'),
    url(r'^login$', 'students.views.login', name='login'),
)
