from django.conf.urls import patterns, url

from choosesomeacts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^acts/', views.showActs, name='Acts Overview'),
	url(r'^fusion/', views.showActsNew, name='Acts Overview New'),
	url(r'^fusion/myacts', views.showMyActs, name='Show my acts by selection'),
	url(r'^update_session', views.update_session, name='AJAX Session Updater'),
)