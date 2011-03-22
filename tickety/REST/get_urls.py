from django.conf.urls.defaults import *

# All GET commands get filtered through this.

urlpatterns = patterns('',
	(r'^city/(.*?)/detector/', 'REST.views.city_detectors'),
	(r'^city/(.*?)/(.*)/$', 'REST.views.city'),
	(r'^city/(.*?)/$', 'REST.views.city'),
	(r'^detector/(.*?)/(.*)/', 'REST.views.detector'),
	(r'^detector/(.*?)/(.*)/', 'REST.views.detector_by_id'),
)
