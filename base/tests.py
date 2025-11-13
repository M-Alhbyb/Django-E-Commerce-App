from django.test import TestCase, RequestFactory
from base.middleware.ipBlocker import IPBlockerMiddleware
from django.http import HttpResponseForbidden

class IPBlockerMiddlewareTests(TestCase):
  def setUp(self):
    self.middleware = IPBlockerMiddleware(get_response=lambda req: None)
    self.factory = RequestFactory()

    self.blacklisted_ip = '100.100.100.100'
    IPBlockerMiddleware.BLACKLISTED_IPS.append(self.blacklisted_ip)
    self.allowed_ip = '200.200.200.200'

  def tearDown(self):
    if self.blacklisted_ip in IPBlockerMiddleware.BLACKLISTED_IPS:
      IPBlockerMiddleware.BLACKLISTED_IPS.remove(self.blacklisted_ip)
  
  def test_blacklisted_ip_is_blocked(self):
    request = self.factory.get('/', REMOTE_ADDR=self.blacklisted_ip)
    response = self.middleware.process_request(request)

    self.assertIsInstance(response, HttpResponseForbidden)
    self.assertEqual(response.status_code, 403)

  def test_allowed_ip_passed_through(self):
    request = self.factory.get('/', REMOTE_ADDR=self.allowed_ip)

    response = self.middleware.process_request(request)
    self.assertIsNone(response)