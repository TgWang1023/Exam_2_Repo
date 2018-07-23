from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.main),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^quote_actions$', views.quote_actions),
    url(r'^add_quote$', views.add_quote),
    url(r'^edit$', views.edit),
    url(r'^update$', views.update),
    url(r'^display/(?P<id>\d+)$', views.display),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^reset$', views.reset)
]