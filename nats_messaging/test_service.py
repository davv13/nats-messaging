"""
This is a test service that will be used to test the message service layer
"""

from nats_messaging.service.message_service import process_message

process_message(b"This is a message from test_service") # Normal message
process_message(b"    ")  # This one should be ignored
