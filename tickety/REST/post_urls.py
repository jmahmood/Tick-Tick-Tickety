from django.conf.urls.defaults import *

# All GET commands get filtered through this.

urlpatterns = patterns('',
	(r'^detector/new/$', 'REST.post.new_detector'),
	(r'^detector/recalibrate/$', 'REST.post.recalibrate_detector'),
	(r'^detector/disable/$', 'REST.post.city'),
	(r'^reading/new/$', 'REST.post.detector'),
	(r'^reading/delete/$', 'REST.post.detector_by_id'),
)
