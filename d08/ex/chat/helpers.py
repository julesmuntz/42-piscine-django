JOIN_SUFFIX = " has joined the chat"
LEAVE_SUFFIX = " has left the chat"
RECENT_CHAT_LIMIT = 3


def join_message_text(username):
    return f"{username}{JOIN_SUFFIX}"


def leave_message_text(username):
    return f"{username}{LEAVE_SUFFIX}"


def format_sent_at(sent_at):
    return sent_at.strftime("%H:%M")


def message_to_client_dict(message):
    return {
        "username": message.user.username,
        "message": message.content,
        "sent_at": format_sent_at(message.sent_at),
        "message_type": "system" if message.is_system else "chat",
    }


def system_event_dict(username, content, sent_at):
    return {
        "username": username,
        "content": content,
        "sent_at": format_sent_at(sent_at) if hasattr(sent_at, "strftime") else sent_at,
        "message_type": "system",
    }


def chat_event_dict(message):
    return {
        "username": message.user.username,
        "content": message.content,
        "sent_at": format_sent_at(message.sent_at),
        "message_type": "chat",
    }
