# Create your views here.
"""
	(r'^city/([a-zA-Z.-\s]+)/detector/', 'REST.views.city_detectors'),
	(r'^city/([a-zA-Z.-\s]+)/(.*)/', 'REST.views.city'),
	(r'^city/([a-zA-Z.-\s]+)/', 'REST.views.city'),
	(r'^detector/([a-zA-Z.-\s]+)/(.*)/', 'REST.views.detector'),
	(r'^detector/(\d+)/(.*)/', 'REST.views.detector_by_id'),
"""

def __extract_date(date):
	try:
		return datetime.strptime(date, '%Y-%m-%d')
	except:
		try:
			return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
		except:
			return False

def __extract_comand(request, ignore_first=4):
	return request.META['PATH_INFO'].split('/')[ignore_first:]

def __valid_commands(command_array):
	def date_test(item):
		try:
			valid_date = datetime.strptime(date, '%Y-%m-%d')
		except:
			return False
	def datetime_test(item):
		try:
			valid_datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
		except:
			return False
	def date_input(item):
		return date_test(item) or datetime_test(item)

	valid = [ 'from', 'to',
		'average','median','mean',
		'alpha','beta','gamma']
	
	for i in command_array:
		if i not in valid and not date_input(i):
			return False
	return True


def invalid_command(request, command):
	pass

def city_district(request, city_slug, district_slug, command=False):
	print command
	pass



def city(request, city_slug, command=False):
	if not command:
		# get the average for the city.
		objects = Detector.objects.filter(location__city=city_slug)
		return output(request, city_slug, objects)

	command = __extract_comand(request)
	if not __valid_command(command):
		return invalid_command(request, command)

	objects = Detector.objects.filter(location__city=city_slug)
	readings = Radiation.objects.filter(detector__in=objects)


	if 'from' in commands:
		# Extract date.
		date_index = commands.index('from') + 1
		date = extract_date(commands[date_index])
		if not date:
			return invalid_command(request, command)
		readings.filter(taken__gt=date)

	if 'to' in commands:
		# Extract date.
		date_index = commands.index('to') + 1
		date = extract_date(commands[date_index])
		if not date:
			return invalid_command(request, command)
		readings.filter(taken__gt=date)
	

	if 'alpha' in commands:
		# Extract alpha radiation only
		readings.filter(particle='alpha')
	elif 'beta' in commands:
		# Extract alpha radiation only
		readings.filter(particle='beta')
	elif 'gamma' in commands:
		# Extract alpha radiation only
		readings.filter(particle='gamma')
	elif 'general' in commands:
		# information from general cpm detectors
		readings.filter(particle='all')
	
	if 'average' in commands:
		readings.aggregate(AVG('cpm'))
	
	if 'median' in commands:
		total = reading.count()
		median = int(round(total / 2))
		median_reading= reading.order_by('cpm')[median]
	


def detector(request, detector_slug, command=False):
	print command
	pass


def detector_by_id(request, detector_id, command=False):
	print command
	pass

