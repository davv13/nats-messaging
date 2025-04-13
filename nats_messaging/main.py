"""
Main entry point to run the NATS subscriber.
"""

import asyncio
import sys
import os

# Ensure we can import internal modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api.nats_subscriber import run as start_subscriber

if __name__ == "__main__":
    print("🚀 Starting NATS Messaging Subscriber...")
    try:
        asyncio.run(start_subscriber())
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print("Application error:", e)