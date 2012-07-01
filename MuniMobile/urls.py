from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MuniMobile.views.index'),
    url(r'^prediction$', 'MuniMobile_app.views.prediction'),
    url(r'^check_predictions$', 'MuniMobile_app.views.check_predictions'),
    # url(r'^MuniMobile/', include('MuniMobile.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
