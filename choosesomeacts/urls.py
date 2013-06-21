from django.conf.urls import patterns, url

from choosesomeacts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='Index, List of available Festivals'),
	url(r'^fusion/', views.showActsNew, name='Acts Overview New'),
	url(r'^myacts/', views.showMyActs, name='Show my acts by selection'),
	url(r'^update_session', views.update_session, name='AJAX Session Updater'),
    url(r'^login/', views.loginUserView, name='The Login window'),
    )