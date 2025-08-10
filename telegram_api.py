# telegram api

import requests
import config

bot_token = config.bot_token
highest_update_id = None  # Store the highest update ID we've processed


def get_next_offset():
    """Get the offset for the next batch of updates"""
    global highest_update_id
    if highest_update_id is None:
        return None  # Get all available updates on first run
    return highest_update_id + 1


def update_highest_update_id(update_id):
    """Update the highest update ID we've processed"""
    global highest_update_id
    if highest_update_id is None or update_id > highest_update_id:
        highest_update_id = update_id


def get_updates(offset=None, limit=None, timeout=None):
    """Get updates from Telegram API"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    payload = {}
    
    if offset is not None:
        payload["offset"] = offset
    if limit is not None:
        payload["limit"] = limit
    if timeout is not None:
        payload["timeout"] = timeout
    
    try:
        response = requests.get(url, params=payload, timeout=timeout+5 if timeout else 30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")
        return None


def send_message(chat_id, text):
    """Send a message to a chat"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get('ok', False)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return False


def get_message_from_update(update):
    """Extract message text from a single update object"""
    try:
        return update.get("message", {}).get("text")
    except (KeyError, AttributeError):
        return None


def get_chatid_from_update(update):
    """Extract chat ID from a single update object"""
    try:
        return update.get("message", {}).get("chat", {}).get("id")
    except (KeyError, AttributeError):
        return None


# Legacy functions for backward compatibility (deprecated - using the new ones above, having these for fallback)
def get_the_message(data):
    """DEPRECATED: Extract message text from API response data"""
    if not data or "result" not in data or not data["result"]:
        return None
    
    # Get the first message from results
    for update in data["result"]:
        return get_message_from_update(update)
    return None


def get_the_chatid(data):
    """DEPRECATED: Extract chat ID from API response data"""
    if not data or "result" not in data or not data["result"]:
        return None
    
    # Get the first chat ID from results
    for update in data["result"]:
        return get_chatid_from_update(update)
    return None


def get_the_updateid(data):
    """DEPRECATED: Extract update ID from API response data"""
    if not data or "result" not in data or not data["result"]:
        return None
    
    for update in data["result"]:
        return update.get('update_id')
    return None
