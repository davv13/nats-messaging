"""
Test NATS publish functionality using asyncio and nats.aio.client.
This test checks if the publish function can send a message to the NATS server.
"""
import asyncio
from nats.aio.client import Client as NATS

async def publish():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    await nc.publish("updates.messages", b"This is a test message from test_publish.py")
    await nc.drain()

asyncio.run(publish())