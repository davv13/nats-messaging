"""
API Layer: Subscribes to the NATS subject and processes incoming messages.
"""

import asyncio
from nats.aio.client import Client as NATS
from nats_messaging.service.message_service import process_message

# Optional parameters:
# - message_processed_event: asyncio.Event used by main.py to track when processing is complete
# - result_queue: asyncio.Queue used to communicate processing result (True/False) back to main.py
async def run(message_processed_event=None, result_queue=None):
    nc = NATS()  # Create NATS client instance

    try:
        # Connect to local NATS server
        await nc.connect("nats://localhost:4222")
        print("[NATS] Connected to nats://localhost:4222")

        # Callback to handle messages received from NATS
        async def message_handler(msg):
            try:
                # Log the incoming raw message (as bytes)
                print(f"[NATS] Received on '{msg.subject}': {msg.data.decode()}")

                # Process the message via service layer, capture result (True = saved, False = ignored)
                result = process_message(msg.data)

                # Send result back to main.py via result_queue, if provided
                if result_queue:
                    await result_queue.put(result)

            except Exception as e:
                # If there's an error during processing, log it and notify main.py with failure (False)
                print("ERROR in message_handler:", e)
                if result_queue:
                    await result_queue.put(False)

            finally:
                # Always set the event to unblock main.py, regardless of outcome
                if message_processed_event:
                    message_processed_event.set()

        # Subscribe to the NATS subject and bind the callback
        await nc.subscribe("updates.messages", cb=message_handler)
        print("[NATS] Subscribed to subject 'updates.messages'")

        # Keep the subscriber running forever (until cancelled)
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        # Handle connection errors gracefully
        print("[NATS] Connection error:", e)

    finally:
        # Clean shutdown of NATS client
        await nc.drain()