"""JSON helpers for account AJAX endpoints (jQuery $.ajax on /account/)."""

from django.http import JsonResponse


def is_ajax_request(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def ajax_json_response(data, *, status=200):
    return JsonResponse(data, status=status)


def ajax_ok(extra=None):
    payload = {"ok": True}
    if extra:
        payload.update(extra)
    return ajax_json_response(payload)
