# Handle all HTTP POST commands that are dealt with by Tick-Tick-Tickety

from django.db.models import Avg, Max, Min, Count
from django.http import HttpResponse
from geigercounter.models import *
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login



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
			try:
				if not unique_slug(request):
					explanation.append("\nThe nickname you have chosen has already been taken.")
			except:
				pass
			try:
				if not acceptable_count(request):
					explanation.append("\nThe countPerMicrosievert must be a numeric value greater than zero.  It actually was: %s" % request.POST['countPerMicrosievert'])
			except:
				pass


			return HttpResponse("Your POST request was malformed. If possible, we explain why:\n%s" % '\n'.join(explanation), mimetype="text/plain", status=400)

		def unique_slug(request):
			try:
				nn = request.POST['nickname']
				return Detector.objects.filter(nickname=nn).count() == 0
			except:
				return False

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
	@csrf_exempt
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
			return HttpResponse("Invalid request", mimetype="text/plain", status=400)
		
		user = authenticate(username=request.POST['nickname'],password=request.POST['password'])

		if not user:
			return HttpResponse("Invalid username/Password", mimetype="text/plain", status=401)
		try:
			if float(request.POST['countPerMicrosievert']) < 0:
				return HttpResponse("Invalid countPerMicrosievert", mimetype="text/plain", status=400)
		except:
			return HttpResponse("Non-numeric countPerMicrosievert", mimetype="text/plain", status=400)
		
		detector = user.detector
		try:
			old_calibration = detector.calibration.filter(enabled=True).get()
			old_calibration.enabled=False
			old_calibration.disabled_on = datetime.now()
			old_calibration.save()
		except:
			pass

		dc = DetectorCalibration()
		dc.countpermicrosievert = request.POST['countPerMicrosievert']
		dc.enabled = True
		dc.detector = detector
		dc.save()
		return HttpResponse("Your content has been saved", mimetype="text/plain", status=200)




	@staticmethod
	def disable(request):
		pass

# Reading "View" class
class R:

	@staticmethod
	@csrf_exempt
	def new(request):
		def type1():
			reading = Radiation()
			reading.cpm = cpm
			if 'particle' in request.POST and request.POST['particle'] in ['alpha','beta','gamma','all']:
				reading.particle = request.POST['particle']
			if 'taken' in request.POST and request.POST['particle'] in ['alpha','beta','gamma','all']:
				reading.particle = request.POST['particle']
			reading.detector = user.detector
			try:
				calibration = detector.calibration.filter(enabled=True).get()
				reading.detector_calibration = calibration
			except:
				pass
			
			reading.save()
			return HttpResponse("Your content has been saved\n%s" % reading.__unicode__() , mimetype="text/plain", status=200)

		def type2():
			reading = Radiation()
			reading.microsievert = microsievert
			if 'particle' in request.POST and request.POST['particle'] in ['alpha','beta','gamma','all']:
				reading.particle = request.POST['particle']
			reading.detector = user.detector
			try:
				calibration = detector.calibration.filter(enabled=True).get()
				reading.detector_calibration = calibration
			except:
				pass
			
			reading.save()
			return HttpResponse("Your content has been saved\n%s" % reading.__unicode__() , mimetype="text/plain", status=200)



		def valid_request():
			if nickname and password and (cpm or microsievert):
				return True
			
			return False

		def valid_cpm():
			try:
				return cpm and int(cpm) >= 0
			except:
				pass
			
			return False

		def valid_microsieverts():
			try:
				ms_test =float(microsievert)
				return microsievert and ms_test >= 0
			except:
				return False

						
		bad_request_type = fail_on_get(request)
		if bad_request_type:
			return bad_request_type

		nickname = request.POST.get('nickname', False)
		password = request.POST.get('password', False)
		cpm = request.POST.get('cpm', False)
		microsievert = request.POST.get('microsievert', False)
		
		if not valid_request():
			return HttpResponse("Invalid request: You must include the nickname, password, and the cpm or microsievert.", mimetype="text/plain", status=400)

		if cpm and microsievert:
			return HttpResponse("Invalid request: Only include the CPM or the microsievert reading pelase.", mimetype="text/plain", status=400)

		user = authenticate(username=request.POST['nickname'],password=request.POST['password'])

		if not user:
			return HttpResponse("Invalid username/password", mimetype="text/plain", status=401)

		if valid_cpm():
			cpm = int(cpm)
			return type1()
		elif valid_microsieverts():
			return type2()
		else:
			return HttpResponse("CPM or Microsievert must be an integer greater than or equal to 0.", mimetype="text/plain", status=400)


	@staticmethod
	def revise(request):
		pass

	@staticmethod
	def delete(request):
		pass


