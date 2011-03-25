#
"""
	(r'^city/([a-zA-Z.-\s]+)/detector/', 'REST.views.city_detectors'),
	(r'^city/([a-zA-Z.-\s]+)/(.*)/', 'REST.views.city'),
	(r'^city/([a-zA-Z.-\s]+)/', 'REST.views.city'),
	(r'^detector/([a-zA-Z.-\s]+)/(.*)/', 'REST.views.detector'),
	(r'^detector/(\d+)/(.*)/', 'REST.views.detector_by_id'),
"""


from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse
from geigercounter.models import *
from datetime import datetime, timedelta
try:
	import simplejson as json
except ImportError:
	import json

class D:

	@staticmethod
	def __create(request):
		pass

	@staticmethod
	def __authorize(request):
		pass

	@staticmethod
	def new(request):
		def new_error(request):
			pass

		def social_radiation_network(request, d):
			pass
		
		def optional_location_info(request, l):
			if 'district' in request.POST:
				l.district = district
			
			if 'address' in request.POST:
				l.address = address

			if 'latitude' in request.POST:
				l.latitude = latitude
			
			if 'longitude' in request.POST:
				l.longitude = longitude
			
			if 'altitude' in request.POST:
				l.altitude = altitude

			l.save()

		def success(request, detector):
			url = "/get/detector/%s/information" % detector.nickname
			helpurl = "/post/help/"
			githuburl = "https://github.com/jmahmood/Tick-Tick-Tickety"
			response = """Your detector was successfully added.  Please remember to note your current password, as it is not possible to retrieve it.
Your Detector Info URL is: %s
Help documentation for posting information is available at: %s
You can see the project page at: %s"""% (url, helpurl, githuburl)
			return HttpResponse(response, mimetype="text/plain", status=201)

		def post(request):
			required = ['nickname','password','cityName','indoorOutdoor','countPerMicrosievert']
			try:
				nickname = request.POST['nickname']
				password = request.POST['password']
				cityname = request.POST['cityName']
				indooroutdoor = request.POST['indoorOutdoor']
				countpermicrosievert = request.POST['countPerMicrosievert']
			except:
				return False
			
			if not unique_slug(request):
				return False
			
			if not acceptable_count(request):
				return False

			l = Location()
			l.city = cityname
			l.indooroutdoor = 1 if indooroutdoor == 'indoor' else 2
			l.save()

			d = Detector()
			d.nickname = nickname
			d.location = l
			d.save()

			dc = DetectorCalibration()
			dc.countpermicrosievert = countpermicrosievert
			dc.enabled = True
			dc.detector = d
			dc.save()

			# optional values

			if 'district' in request.POST or 'address' in request.POST or 'latitude' in request.POST \
			or 'longitude' in request.POST or 'altitude' in request.POST:
				optional_location_info(request, l)


			if 'email' in request.POST or 'twitter' in request.POST or 'description' in request.POST:
				social_radiation_network(request, d)
			
			return d
		


		detector = post(request)
		if not detector:
			return new_error(request)
		else:
			return success(request, detector)

	@staticmethod
	def recalibrate(request):
		pass

	@staticmethod
	def disable(request):
		pass

class R:

	@staticmethod
	def new(request):
		pass

	@staticmethod
	def revise(request):
		pass

	@staticmethod
	def delete(request):
		pass


