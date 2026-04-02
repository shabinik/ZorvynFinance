from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    return Response(
        {
            "success": False,
            "message": _extract_message(response.data),
            "errors": response.data,
        },
        status=response.status_code,
    )


def _extract_message(data) -> str:
    if isinstance(data, dict):
        if "detail" in data:
            return str(data["detail"])

        for key, value in data.items():
            if isinstance(value, list) and value:
                return f"{key}: {value[0]}"
            return f"{key}: {value}"

    if isinstance(data, list) and data:
        return str(data[0])

    return "An error occurred."