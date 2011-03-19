from django.conf.urls.defaults import *

# All GET commands get filtered through this.

urlpatterns = patterns('',
	(r'^city/([\w|\W]+)/detector/', 'REST.views.city_detectors'),
	(r'^city/([\w|\W]+)/(.*)', 'REST.views.city'),
	(r'^city/([\w|\W]+)/', 'REST.views.city'),
	(r'^detector/([\w|\W]+)/(.*)/', 'REST.views.detector'),
	(r'^detector/(\d+)/(.*)/', 'REST.views.detector_by_id'),
)
