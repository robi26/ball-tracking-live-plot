#!/usr/bin/env python3
"""Simple OSC receiver test - minimal setup to verify OSC communication."""

import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def default_handler(address, *args):
    """Handle any OSC message."""
    print(f"📩 Received OSC: {address} -> {args}")


def main():
    parser = argparse.ArgumentParser(description="Simple OSC Test Receiver")
    parser.add_argument("--host", default="127.0.0.1", help="OSC server host")
    parser.add_argument("--port", type=int, default=9999, help="OSC server port")
    args = parser.parse_args()
    
    print(f"🎧 Starting OSC server on {args.host}:{args.port}")
    print("Listening for all OSC messages...")
    print("Press Ctrl+C to stop\n")
    
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(default_handler)
    
    server = BlockingOSCUDPServer((args.host, args.port), dispatcher)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Stopping OSC server...")


if __name__ == "__main__":
    main()
