from datetime import datetime
from d06.settings import SESSION_EXPIRE_SECONDS


def session_timeout(request):
    """
    Context processor to calculate remaining session time.
    Makes 'session_remaining_seconds' available in all templates.
    """
    remaining_seconds = None

    if request.session.session_key:
        session_init = request.session.get("_session_init_timestamp_")

        if session_init:
            current_time = datetime.now().timestamp()
            elapsed_time = current_time - session_init
            remaining_seconds = max(0, int(SESSION_EXPIRE_SECONDS - elapsed_time))

    return {
        "session_remaining_seconds": remaining_seconds,
        "session_total_seconds": SESSION_EXPIRE_SECONDS,
    }
