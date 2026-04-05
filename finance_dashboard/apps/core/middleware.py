import time
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        user = request.user if request.user.is_authenticated else "Anonymous"

        logger.info(
            f"{request.method} {request.path} | "
            f"User: {user} | "
            f"Status: {response.status_code} | "
            f"Time: {duration:.2f}s"
        )

        return response