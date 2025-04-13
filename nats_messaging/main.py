"""
Main entry point for the NATS Messaging CLI Application.

- Starts the subscriber via run() from nats_subscriber.py
- Provides CLI for sending messages to 'updates.messages'
- All processing and saving is handled downstream via 3-layer architecture
"""

import asyncio
import time
from nats.aio.client import Client as NATS
from nats_messaging.api.nats_subscriber import run as start_subscriber

async def main():
    # Event used to signal when the subscriber finishes processing a message
    message_processed_event = asyncio.Event()

    # Queue to receive boolean result (True = saved, False = ignored)
    result_queue = asyncio.Queue()

    print("✨ Starting NATS Messaging CLI App...\n")

    # Start subscriber in the background and pass both signaling mechanisms
    subscriber_task = asyncio.create_task(
        start_subscriber(message_processed_event, result_queue)
    )

    # Small delay to allow subscriber to connect and print its status
    await asyncio.sleep(1)

    # Initialize publisher connection to NATS
    publisher_nc = NATS()
    await publisher_nc.connect("nats://localhost:4222")

    while True:
        # Get user input from terminal in a non-blocking way
        message = await asyncio.get_event_loop().run_in_executor(
            None, input, "\n💬 Type a message to publish to 'updates.messages' (type 'exit' to quit):\n📤 > "
        )
        message = message.strip()

        if message.lower() == "exit":
            print("👋 Exiting publisher...")
            break

        if message:
            # Clear the event flag before publishing
            message_processed_event.clear()

            # Publish the message to the NATS subject
            await publisher_nc.publish("updates.messages", message.encode())

            # Wait until subscriber has handled the message
            await message_processed_event.wait()

            # Read result from the subscriber via result_queue
            try:
                result = await asyncio.wait_for(result_queue.get(), timeout=1)
                if result:
                    print("✅ Message processed and saved.")
                else:
                    print("⚠️  Message was ignored (empty or whitespace).")
            except asyncio.TimeoutError:
                print("⚠️  No result received from subscriber.")
        else:
            # User entered only empty or whitespace input
            print("⚠️  Message was empty. Nothing was sent.")

    # Cleanly close NATS publisher connection
    await publisher_nc.drain()

    # Cancel and gracefully shut down the subscriber
    subscriber_task.cancel()
    try:
        await subscriber_task
    except asyncio.CancelledError:
        print("🛑 Subscriber stopped.")

# Standard entry point
if __name__ == "__main__":
    try:
        # Small startup delay to improve terminal output alignment
        time.sleep(1)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    except Exception as e:
        print("❌ Application error:", e)