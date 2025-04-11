import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nats_messaging.data.message_repository import save_message

# Test message
save_message("This is a test message from Davit!")
save_message("Hello World!")
save_message("New message!")

