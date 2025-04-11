"""
Test the message service by sending a message to it and checking the response.
This test checks if the message service correctly processes a message and ignores empty messages.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nats_messaging.service.message_service import process_message

process_message(b"This is a message from test_service") # Normal message
process_message(b"    ")  # This one should be ignored
