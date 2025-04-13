"""
Service Layer: Processes incoming messages before saving them to the database.
"""

from nats_messaging.data.message_repository import save_message

def process_message(message):
    """
    Decodes, cleans, and validates an incoming message before saving it.
    Returns:
        bool: True if message saved, False if ignored
    """
    try:
        # Decode if it's a byte stream (as NATS sends)
        content = message.decode() if isinstance(message, bytes) else str(message)
        # Remove leading/trailing whitespace
        content = content.strip()

        # Validate content is not empty after stripping
        if content:
            save_message(content)
            return True
        else:
            print("[Service] Ignored empty or whitespace-only message.")
            return False

    except Exception as e:
        print("[Service] Error processing message:", e)
        return False
