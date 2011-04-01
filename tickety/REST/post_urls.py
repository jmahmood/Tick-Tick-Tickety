from django.conf.urls.defaults import *

# All GET commands get filtered through this.
from post import D, R

urlpatterns = patterns('',
	(r'^detector/new/$', D.new),
	(r'^detector/recalibrate/$', D.recalibrate),
	(r'^detector/disable/$', D.disable),
	(r'^reading/new/$', R.new),
	(r'^reading/revise/$', R.revise),
	(r'^reading/delete/$', R.delete),
)
