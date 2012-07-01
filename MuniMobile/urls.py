from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MuniMobile_app.views.index'),
    url(r'^prediction$', 'MuniMobile_app.views.prediction'),
    url(r'^check_predictions$', 'MuniMobile_app.views.check_predictions'),
    url(r'^get_all_routes$', 'MuniMobile_app.views.get_all_routes'),
    url(r'^get_directions_of_route$', 'MuniMobile_app.views.get_directions_of_route'),
    url(r'^get_stops$', 'MuniMobile_app.views.get_stops'),
    url(r'^get_predictions_for_stop$', 'MuniMobile_app.views.get_predictions_for_stop'),
    url(r'^set_notification$', 'MuniMobile_app.views.set_notification'),
)
