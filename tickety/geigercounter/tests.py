"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class DetectorPostTest(TestCase):
	def test_get(self):
		url = '/post/detector/new/'
		c = Client()
		response = c.get(url)
		self.failUnlessEqual(response.status_code, 405)

	def test_invalid_post(self):
		url = '/post/detector/new/'
		c = Client()
		response = c.post(url,{})
		self.failUnlessEqual(response.status_code, 400)
