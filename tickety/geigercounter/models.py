from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
	INSIDEOUTSIDE = ( (1,'Inside'), (2,'Outside'), )

	city = models.CharField( verbose_name = 'City', max_length=45)
	district = models.CharField( verbose_name = 'District', max_length=45, blank=True, null=True)
	insideoutside = models.IntegerField( verbose_name='Located Indoors or Outdoors?', choices=INSIDEOUTSIDE)

	address = models.CharField( verbose_name='Address', max_length=45, blank=True, null=True)
	lat = models.DecimalField( verbose_name="Latitude", max_digits=11, decimal_places=6, blank=True, null=True)
	lon = models.DecimalField( verbose_name="Longitude", max_digits=11, decimal_places=6, blank=True, null=True)
	altitude = models.IntegerField( verbose_name="Altitude", blank=True, null=True)

	def __unicode__(self):
		return "%s (%s)" %(self.city,self.get_insideoutside_display())

class DetectorSocial(models.Model):
	#because someone somewhere is going to want a social network for geiger nerds
	detector = models.ForeignField(Detector, related_name="Social")
	description = models.TextField(blank=True, null=True)
	twitter = models.CharField(max_length=40, blank=True, null=True)


# Store calibration data for a model detector to allow conversion between CPM to microsievert/hour.
class DetectorCalibration(models.Model):
	countpermicrosievert = models.FloatField( verbose_name="microsieverts")
	enabled = models.BooleanField(default=True)
	detector = models.ForeignField(Detector, related_name="calibration")
	created = models.DateTimeField(auto_now_add=True)
	disabled_on = models.DateTimeField(blank=True, null=True)

	def ratio(self):
		return self.microsievert / self.count


class Detector(models.Model):
	nickname = models.SlugField()
	location = models.OneToOneField(Location, verbose_name="Positional Information")
	enabled = models.BooleanField(default=False)
	added = models.DateTimeField(auto_now_add=True)
	owner = models.OneToOneField(User, related_name="detector")

	def __unicode__(self):
		return "%s (%s)" %(self.nickname,self.location)

# Base class to store readings taken
class Radiation(models.Model):
	class Meta:
		get_latest_by = "taken"
		ordering=['taken','particle']
		verbose_name="Radioactivity Reading"
		verbose_name_plural="Radioactivity Readings"

	RADIOACTIVE_PARTICLES = ( ('alpha','Alpha Particles'), ('beta','Beta Particles'), ('gamma','Gamma Particles'), ('all','All'))
	cpm = models.IntegerField(verbose_name="Counts per Minute")
	added = models.DateTimeField(auto_now_add=True)
	taken = models.DateTimeField(verbose_name="Date/Time the readings are taken")
	detector = models.ForeignKey(Detector, related_name="detected")
	detector_callibration = models.ForeignKey(DetectorCalibration, verbose_name="Detector Calibration when readings were taken")
	particle = models.CharField(max_length=10, choices=RADIOACTIVE_PARTICLES, default='all')

	def __unicode__(self):
		return "%s: Radiation CPM: %d" % (self.detector, self.cpm)
