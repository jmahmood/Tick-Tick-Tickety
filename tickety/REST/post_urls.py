from django.conf.urls.defaults import *

# All GET commands get filtered through this.

urlpatterns = patterns('',
	(r'^detector/new/$', 'REST.views.new_detector'),
	(r'^detector/recalibrate/$', 'REST.views.recalibrate_detector'),
	(r'^detector/disable/$', 'REST.views.city'),
	(r'^reading/new/$', 'REST.views.detector'),
	(r'^reading/delete/$', 'REST.views.detector_by_id'),
)
