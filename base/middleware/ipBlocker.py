from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class IPBlockerMiddleware(MiddlewareMixin):
  BLACKLISTED_IPS = [
        '192.168.1.100',  
        '10.0.0.50',      
    ]
  
  def process_request(self, request):
    client_ip = request.META.get('REMOTE_ADDR')
    if client_ip in self.BLACKLISTED_IPS:
      print(f"IP BLOCKED: Forbidden access attempt from {client_ip} to {request.path}")
      return HttpResponseForbidden("Access Denied: Your IP address has been blacklisted.")
    
    return None