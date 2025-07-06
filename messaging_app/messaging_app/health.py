from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Health check endpoint that verifies database connectivity."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"status": "ok", "database": "connected"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "database": "disconnected", "error": str(e)}, status=500)
