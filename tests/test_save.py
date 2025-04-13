"""
Test the save_message function from the message_repository module.
This test checks if the function correctly saves messages to a file.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nats_messaging.data.message_repository import save_message

# Test message
save_message("This is a test message from test_save.py")