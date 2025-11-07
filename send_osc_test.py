#!/usr/bin/env python3
"""Quick test to send a single OSC message to verify connection."""

import argparse
import time
from pythonosc import udp_client


def main():
    parser = argparse.ArgumentParser(description="Send test OSC message")
    parser.add_argument("--host", default="127.0.0.1", help="OSC server host")
    parser.add_argument("--port", type=int, default=9999, help="OSC server port")
    args = parser.parse_args()
    
    print(f"📤 Sending test OSC messages to {args.host}:{args.port}")
    
    client = udp_client.SimpleUDPClient(args.host, args.port)
    
    # Send a few test messages
    for i in range(5):
        client.send_message("/test/message", [i, i * 10, f"test_{i}"])
        print(f"   Sent message #{i}")
        time.sleep(0.5)
    
    print("✅ Done sending test messages")


if __name__ == "__main__":
    main()
