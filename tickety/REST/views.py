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


def __extract_date(date):
	try:
		return datetime.strptime(date, '%Y-%m-%d')
	except:
		try:
			return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
		except:
			return False

def __extract_commands(request, ignore_first=4):
	path_info = request.META['PATH_INFO']
	if path_info.endswith('/'):
		path_info = path_info[:-1]
	print path_info
	return path_info.split('/')[ignore_first:]

def __valid_commands(command_array):
	def date_test(date):
		try:
			valid_date = datetime.strptime(date, '%Y-%m-%d')
			return True
		except:
			return False
	def datetime_test(item):
		try:
			valid_datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
			return True
		except:
			return False
	def date_input(item):
		return date_test(item) or datetime_test(item)

	valid = [ 'from', 'to',
		'average','median','mean',
		'alpha','beta','gamma',
		'xml','json']
	
	for i in command_array:
		if i not in valid and not date_input(i):
			return False
	return True


def invalid_command(request, command):
	return HttpResponse("Invalid command! %s" % command)

def json_one_reading(request, city_slug, name, reading):
	output_array = []
	output_array.append(
		{name:reading}
	)
	output = json.dumps(output_array)
	return HttpResponse(output)

def xml_output (request, city_slug, detectors, readings):
	return HttpResponse("XML is worthless.  Sorry.")

def output (request, city_slug, detectors, readings):
	output_array = []
	for r in readings:
		output_array.append(
			{
				'detector_nickname':r.detector.nickname,
				'timestamp':r.taken.strftime('%Y-%m-%d %H:%M:%S'),
				'amount':r.cpm,
				'radiation_type':r.particle,
			}
		)
	output = json.dumps(output_array)
	return HttpResponse(output)

def city_detectors(request, city_slug):
	pass

def city_district(request, city_slug, district_slug, command=False):
	pass

def city(request, city_slug, commands=False):

	# The current Regex needs to be fixed.
	# It sometimes passes in a city name like
	# Tokyo/alpha or some other nonsense like that.
	# This command cleans up the city name, but
	# ideally should not be needed


	detectors = Detector.objects.filter(location__city=city_slug)

	if 'indoors' in commands:
		# indoor detectors ONLY
		detectors = detectors.filter(location__insideoutside=1)
	if 'outdoors' in commands:
		# outdoor detectors ONLY
		detectors = detectors.filter(location__insideoutside=2)

	readings = Radiation.objects.filter(detector__in=detectors)

	if not commands:
		# get the info for the city for the past week.
		readings = readings.filter(taken__gte=datetime.now() - timedelta(weeks=1))
		return output(request, city_slug, detectors, readings)
	
	commands = __extract_commands(request)

	if not __valid_commands(commands):
		return invalid_command(request, commands)

	if 'from' in commands:
		# Extract date.
		date_index = commands.index('from') + 1
		date = __extract_date(commands[date_index])
		if not date:
			return invalid_command(request, command)

		readings = readings.filter(taken__gte=date)

	if 'to' in commands:
		# Extract date.
		date_index = commands.index('to') + 1
		date = __extract_date(commands[date_index])
		if not date:
			return invalid_command(request, command)

		readings = readings.filter(taken__lte=date + timedelta(days=1))

	if 'alpha' in commands:
		# Extract alpha radiation only
		readings = readings.filter(particle='alpha')
	elif 'beta' in commands:
		# Extract alpha radiation only
		readings = readings.filter(particle='beta')
	elif 'gamma' in commands:
		# Extract alpha radiation only
		readings = readings.filter(particle='gamma')
	elif 'general' in commands:
		# information from general cpm detectors
		readings = readings.filter(particle='all')
	
	print readings

	if 'average' in commands:
		average = readings.aggregate(Avg('cpm'))
		if 'xml' in commands:
			return xml_one_reading(request, city_slug, "Average Reading", average)
		return json_one_reading(request, city_slug,"Average Reading",  average['cpm__avg'])


	if 'median' in commands:
		total = readings.count()
		median = int(round(total / 2))
		median_reading= readings.order_by('cpm')[median]
		if 'xml' in commands:
			return xml_one_reading(request, city_slug, "Median Reading", median_reading)
		return json_one_reading(request, city_slug,"Median Reading",  median_reading.cpm)


	if 'xml' in commands:
		return xml_output(request, city_slug, detectors, readings)

	return output(request, city_slug, detectors, readings)

def detector(request, detector_slug, command=False):
	print command
	pass


def detector_by_id(request, detector_id, command=False):
	print command
	pass

