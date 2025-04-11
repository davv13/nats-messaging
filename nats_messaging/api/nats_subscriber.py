"""
API Layer: Subscribes to the NATS subject and processes incoming messages.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import asyncio
from nats.aio.client import Client as NATS
from nats_messaging.service.message_service import process_message

async def run():
    nc = NATS()

    try:
        # Connect to local NATS server
        await nc.connect("nats://localhost:4222")
        print("[NATS] Connected to nats://localhost:4222")

        # Define a callback for incoming messages
        async def message_handler(msg):
            print(f"[NATS] Received on '{msg.subject}': {msg.data.decode()}")
            process_message(msg.data)

        # Subscribe to a subject
        await nc.subscribe("updates.messages", cb=message_handler)
        print("[NATS] Subscribed to subject 'updates.messages'")

        # Keep running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print("[NATS] Connection error:", e)
    finally:
        await nc.drain()

if __name__ == "__main__":
    asyncio.run(run())
