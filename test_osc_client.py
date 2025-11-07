#!/usr/bin/env python3
"""Direct test of ball_tracking OSC functionality."""

import logging
from ball_tracking.osc_client import OSCClient

# Enable debug logging
logging.basicConfig(level=logging.INFO)

print("=" * 60)
print("Ball Tracking OSC Client Test")
print("=" * 60)

# Create OSC client
print("\n📤 Creating OSC client...")
osc_client = OSCClient(host="127.0.0.1", port=9999, enabled=True)

if not osc_client.enabled:
    print("❌ OSC client failed to initialize!")
    exit(1)

print("✅ OSC client initialized\n")

# Send test ball positions
print("Sending test ball positions...")
for i in range(5):
    x, y = 320 + i * 20, 240 + i * 15
    osc_client.send_ball_position((x, y), 640, 480)
    
print("\nSending ball lost signal...")
osc_client.send_ball_lost()

print("\nSending tracking info...")
osc_client.send_tracking_info(30.0, 150)

print("\n" + "=" * 60)
print("✅ Test complete! Check your OSC server to see if messages arrived.")
print("=" * 60)
