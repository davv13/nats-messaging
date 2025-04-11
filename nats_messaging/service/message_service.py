"""
Service Layer: Processes incoming messages before saving them to the database.
"""

from nats_messaging.data.message_repository import save_message

def process_message(message):
    """
    Decodes, cleans, and validates an incoming message before saving it.

    Parameters:
    ----------
    message : bytes or str
        The raw message data received (typically from NATS).
    """
    try:
        # Decode if it's a byte stream (as NATS sends)
        content = message.decode() if isinstance(message, bytes) else str(message)

        # Remove leading/trailing whitespace
        content = content.strip()

        # Validate content is not empty after stripping
        if content:
            save_message(content)
        else:
            print("[Service] Ignored empty or whitespace-only message.")

    except Exception as e:
        print("[Service] Error processing message:", e)
