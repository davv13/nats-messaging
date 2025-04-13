"""
Test NATS publish functionality with user input.
You can type your own message to be sent to the NATS subject 'updates.messages'.
"""

import asyncio
from nats.aio.client import Client as NATS

async def publish():
    message = input("💬 Enter the message to publish to 'updates.messages': ").strip()

    if not message:
        print("⚠️  Message is empty. Exiting.")
        return

    nc = NATS()
    await nc.connect("nats://localhost:4222")
    await nc.publish("updates.messages", message.encode())
    await nc.drain()
    print(f"✅ Message sent: {message}")

if __name__ == "__main__":
    asyncio.run(publish())