from datetime import datetime
from home.views import is_anonymous_session


def session_timeout(request):
    """
    Context processor to calculate remaining session time.
    Makes 'session_remaining_seconds' available in all templates.
    """
    remaining_seconds = None
    total_seconds = -1
    if is_anonymous_session(request):
        total_seconds = 42

    if request.session.session_key and total_seconds > 0:
        session_init = request.session.get("_session_init_timestamp_")

        if session_init:
            current_time = datetime.now().timestamp()
            elapsed_time = current_time - session_init
            remaining_seconds = "%.2f" % max(0, float(total_seconds - elapsed_time))

    return {
        "session_remaining_seconds": remaining_seconds,
        "session_total_seconds": total_seconds,
    }
