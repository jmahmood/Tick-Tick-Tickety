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
from django.views.decorators.csrf import csrf_exempt


try:
	import simplejson as json
except ImportError:
	import json

def __glogin(request):
	username = request.POST['nickname']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			return user
		else:
			return False
	else:
		return False

def fail_on_get(request):
	if request.method == 'GET':
		return HttpResponse("You must make an HTTP POST call to execute this request", mimetype="text/plain", status=405)
	return False



class D:

	@staticmethod
	def __create(request):
		pass

	@staticmethod
	def __authorize(request):
		pass

	@staticmethod
	@csrf_exempt
	def new(request):
		bad_request_type = fail_on_get(request)
		if bad_request_type:
			return bad_request_type

		def acceptable_count(request):
			try:
				float(request.POST['countPerMicrosievert'])
				return request.POST['countPerMicrosievert'] > 0
			except:
				return False

		def valid_request(request):
			try:
				nickname = request.POST['nickname']
				password = request.POST['password']
				cityname = request.POST['cityName']
				insideoutside = request.POST['insideOutside']
				countpermicrosievert = request.POST['countPerMicrosievert']
			except:
				return False
			return True


		def new_error(request):
			explanation = ['Debugging']

			if not valid_request(request):
				explanation.append("\nYou must include a nickname, password, cityname, inside/outside and the count per microsievert.")
			if not unique_slug(request):
				explanation.append("\nThe nickname you have chosen has already been taken.")
			if not acceptable_count(request):
				explanation.append("\nThe countPerMicrosievert must be a numeric value greater than zero.  It actually was: %s" % request.POST['countPerMicrosievert'])


			return HttpResponse("Your POST request was malformed. If possible, we explain why:\n%s" % '\n'.join(explanation), mimetype="text/plain", status=400)

		def unique_slug(request):
			nn = request.POST['nickname']
			return Detector.objects.filter(nickname=nn).count() == 0

		def social_radiation_network(request, d):
			ds = DetectorSocial()
			ds.detector = d

			if 'email' in request.POST:
				ds.email = request.POST['email']
			
			if  'twitter' in request.POST:
				ds.twitter = request.POST['twitter']
			
			if 'description' in request.POST:
				ds.description = request.POST['description']
			
			ds.save()
		
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
			l = Location()
			l.city = request.POST['cityName']
			l.insideoutside = 1 if request.POST['insideOutside'] == 'inside' else 2
			l.save()

			o =User()
			o.username = request.POST['nickname']
			o.set_password(request.POST['password'])
			o.save()

			d = Detector()
			d.nickname = request.POST['nickname']
			d.location = l
			d.owner = o
			d.save()


			dc = DetectorCalibration()
			dc.countpermicrosievert = request.POST['countPerMicrosievert']
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
		


		if not valid_request(request) or not unique_slug(request) or  not acceptable_count(request):
			return new_error(request)

		detector = post(request)

		if not detector:
			return new_error(request)
		else:
			return success(request, detector)

	@staticmethod
	def recalibrate(request):
		def valid_request(request):
			try:
				nickname = request.POST['nickname']
				password = request.POST['password']
				countpermicrosievert = request.POST['countPerMicrosievert']
			except:
				return False
			return True
		
		if not valid_request(request):
			return error400(request)
		
		user = __glogin(request)
		if not user:
			return error401(request)
		
		try:
			if float(request.POST['countPerMicrosievert']) < 0:
				return error401(request)
		except:
			return error400(request)
		
		detector = user.detector.get()
		old_calibration = detector.calibration.filter(enabled=False)
		old_calibration.enabled=False
		old_calibration.disabled_on = datetime.now()

		dc = DetectorCalibration()
		dc.countpermicrosievert = request.POST['countPerMicrosievert']
		dc.enabled = True
		dc.detector = detector
		dc.save()
		old_calibration.save()




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


