from datetime import datetime, time
from django.http import HttpResponseForbidden
import logging
from collections import defaultdict
import time as time_module

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='requests.log'
)

class RequestLoggingMiddleware:
    """
    Middleware to log all incoming requests with timestamp, user, and path.
    Logs are saved to requests.log in the project root directory.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        logger.info(f"User: {user} - Path: {request.path} - Method: {request.method}")
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to chat endpoints between 9 PM and 6 AM.
    Returns 403 Forbidden if accessed outside allowed hours.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(21, 0)  # 9 PM
        end_time = time(6, 0)     # 6 AM
        
        # Check if the request is for chat endpoints and outside allowed hours
        if (current_time > start_time or current_time < end_time) and request.path.startswith('/chat/'):
            return HttpResponseForbidden(
                "Chat access is only allowed between 6 AM and 9 PM. "
                f"Current time: {current_time.strftime('%H:%M')}"
            )
        
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware that implements rate limiting for chat messages.
    Limits users to 5 messages per minute based on IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = defaultdict(list)
        self.LIMIT = 5  # 5 requests
        self.WINDOW = 60  # 60 seconds

    def __call__(self, request):
        # Only process POST requests to chat endpoints
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip = request.META.get('REMOTE_ADDR')
            current_time = time_module.time()
            
            # Clean up old requests outside the time window
            self.request_counts[ip] = [t for t in self.request_counts.get(ip, []) 
                                     if current_time - t < self.WINDOW]
            
            # Check if rate limit is exceeded
            if len(self.request_counts.get(ip, [])) >= self.LIMIT:
                return HttpResponseForbidden(
                    "Rate limit exceeded. Maximum 5 messages per minute allowed. "
                    "Please try again later."
                )
            
            # Log the request time
            self.request_counts[ip].append(current_time)
        
        return self.get_response(request)


class RolePermissionMiddleware:
    """
    Middleware that enforces role-based access control.
    Restricts certain paths to admin users only.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of admin-only paths
        admin_paths = ['/admin/', '/chat/admin/']  # Add your admin paths here
        
        # Check if the current path requires admin access
        if any(request.path.startswith(path) for path in admin_paths):
            if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
                return HttpResponseForbidden(
                    "You don't have permission to access this page. "
                    "Admin or staff privileges required."
                )
        
        return self.get_response(request)
