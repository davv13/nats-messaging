"""
API Layer: Subscribes to the NATS subject and processes incoming messages.
"""

import asyncio
from nats.aio.client import Client as NATS
from nats_messaging.service.message_service import process_message

async def run():
    nc = NATS()

    try:
        await nc.connect("nats://localhost:4222")
        print("[NATS] Connected to nats://localhost:4222")

        async def message_handler(msg):
            try:
                print(f"[NATS] Received on '{msg.subject}': {msg.data.decode()}")
                process_message(msg.data)
            except Exception as e:
                print("ERROR in message_handler:", e)

        await nc.subscribe("updates.messages", cb=message_handler)
        print("[NATS] Subscribed to subject 'updates.messages'")

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print("[NATS] Connection error:", e)
    finally:
        await nc.drain()
