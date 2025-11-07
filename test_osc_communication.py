#!/usr/bin/env python3
"""Comprehensive OSC communication test."""

import time
from pythonosc import udp_client

print("=" * 60)
print("OSC Communication Test")
print("=" * 60)

# Test configuration
host = "127.0.0.1"
port = 9999

print(f"\n📤 Creating OSC client to send to {host}:{port}")
print("   Make sure you have an OSC server running on this port!")
print("   (Run: uv run python simple_osc_test.py --port 9999)\n")

input("Press Enter when OSC server is ready...")

try:
    client = udp_client.SimpleUDPClient(host, port)
    print("✅ OSC client created successfully\n")
    
    # Test 1: Simple message
    print("Test 1: Sending simple test message...")
    client.send_message("/test/simple", ["Hello OSC!"])
    time.sleep(0.5)
    
    # Test 2: Ball position (like in tracking)
    print("Test 2: Sending ball position messages...")
    for i in range(3):
        x, y = 320 + i * 10, 240 + i * 10
        client.send_message("/ball/position/raw", [x, y])
        client.send_message("/ball/position/normalized", [x/640, y/480])
        print(f"   Sent ball position: ({x}, {y})")
        time.sleep(0.5)
    
    # Test 3: Tracking info
    print("Test 3: Sending tracking info...")
    client.send_message("/ball/tracking/fps", [30.0])
    client.send_message("/ball/tracking/frame", [100])
    time.sleep(0.5)
    
    # Test 4: Ball lost
    print("Test 4: Sending ball lost signal...")
    client.send_message("/ball/lost", [True])
    time.sleep(0.5)
    
    print("\n✅ All test messages sent!")
    print("   Check your OSC server terminal to see if messages were received.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("   Make sure the OSC server is running!")

print("\n" + "=" * 60)
