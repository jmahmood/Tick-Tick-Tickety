"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from geigercounter.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class DetectorPostTest(TestCase):
	def setUp(self):
		self.detector = Detector()
		self.detector.nickname = 'pre-existing'
		location = Location()
		location.city='Tokyo'
		location.insideoutside=1
		location.save()
		self.detector.location = location

		user = User()
		user.username='pre-existing'
		user.set_password('validpassword')
		user.save()

		self.detector.owner = user
		self.detector.enabled=True
		self.detector.save()

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

	def test_valid_post(self):
		url = '/post/detector/new/'
		c = Client()
		response = c.post(url,{'nickname':'test','password':'test2','cityName':'Tokyo','insideOutside':'inside','countPerMicrosievert':20.0})
		a = User.objects.get(username='test') # <avu> jbm_tokyo, the tests fail if an exception is raised anyway
		self.assertEqual(response.status_code, 201)
		self.assertNotEqual(authenticate(username='test',password='test2'), None)

	def test_valid_recalibration(self):
		url = '/post/detector/recalibrate/'
		c = Client()
		self.assertNotEqual(authenticate(username='pre-existing',password='validpassword'), None)
		response = c.post(url,{'nickname':'pre-existing','password':'validpassword','countPerMicrosievert':25.0})
		self.assertEqual(response.status_code, 200)

	def test_invalid_recalibration(self):
		url = '/post/detector/recalibrate/'
		c = Client()
		self.assertEqual(authenticate(username='pre-existing',password='incorrectpassword'), None)
		response = c.post(url,{'nickname':'pre-existing','password':'incorrectpassword','countPerMicrosievert':25.0})
		self.assertEqual(response.status_code, 401)

	def test_empty_recalibration(self):
		url = '/post/detector/recalibrate/'
		c = Client()
		response = c.post(url,{})
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.content, 'Invalid request')

	def test_invalid_cpms(self):
		url = '/post/detector/recalibrate/'
		c = Client()
		response = c.post(url,{'nickname':'pre-existing','password':'validpassword','countPerMicrosievert':-25.0})
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.content, 'Invalid countPerMicrosievert')
		response = c.post(url,{'nickname':'pre-existing','password':'validpassword','countPerMicrosievert':'lol, word'})
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.content, 'Non-numeric countPerMicrosievert')
