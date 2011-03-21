from models import *
from django.contrib import admin

class CorporateNodeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__')

admin.site.register(Radiation)
admin.site.register(Detector)
admin.site.register(Location)
