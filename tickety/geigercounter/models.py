from django.db import models

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


class Detector(models.Model):

	nickname = models.SlugField()
	location = models.OneToOneField(Location, verbose_name="Positional Information")
	enabled = models.BooleanField(default=False)
	added = models.DateTimeField(auto_now_add=True)

# Base class to store readings taken
class Radiation(models.Model):
	RADIOACTIVE_PARTICLES = ( ('alpha','Alpha Particles'), ('beta','Beta Particles'), ('gamma','Gamma Particles'), ('all','All'))
	cpm = models.IntegerField(verbose_name="Counts per Minute")
	added = models.DateTimeField(auto_now_add=True)
	taken = models.DateTimeField(verbose_name="Date/Time the readings are taken")
	detector = models.ForeignKey(Detector, related_name="detected")
	particle = models.CharField(max_length=10, choices=RADIOACTIVE_PARTICLES, default='all')

	def __unicode__(self):
		return "Radiation CPM: %d" % self.cpm
