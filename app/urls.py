from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^donation', views.donation, name='donation'),
    url(r'^createdonation', views.createDonation, name='createDonation'),
    url(r'^browse', views.browse, name='browse'),
    url(r'^users', views.browse, name='users'),
    url(r'^map', views.map, name='map'),
    url(r'^getDonations', views.getDonations, name='getDonations'),
    url(r'^register', views.register, name='register'),
    url(r'^registerfb', views.registerfb, name='register-facebook')
)
