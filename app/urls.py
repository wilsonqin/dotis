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
    url(r'^users', views.users, name='users'),
    url(r'^map', views.map, name='map'),
    url(r'^getDonations', views.getDonations, name='getDonations'),
    url(r'^collection/(?P<collection_id>[0-9A-Za-z]+)', views.collection, name='collection'),
    url(r'^register', views.register, name='register'),
    # url(r'^registerfb', views.registerfb, name='register-facebook'),
	url(r'^about', views.about, name='about'),

    #populate links
    url(r'^populate/charities', views.populate_food, name='populate charities'),
    url(r'^populate/collection', views.populate_collection, name='populate_collection'),
)
