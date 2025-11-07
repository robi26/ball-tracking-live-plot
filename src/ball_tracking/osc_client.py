"""OSC (Open Sound Control) client for sending ball tracking data to Unreal Engine."""

import logging
from typing import Optional

from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder

from ball_tracking.core import Point2D


class OSCClient:
    """OSC client for sending ball coordinates to Unreal Engine."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 9999, enabled: bool = True):
        """Initialize OSC client.
        
        Args:
            host: IP address of the Unreal Engine OSC server (default: localhost)
            port: Port number of the Unreal Engine OSC server (default: 9999)
            enabled: Whether OSC communication is enabled
        """
        self.host = host
        self.port = port
        self.enabled = enabled
        self.client: Optional[udp_client.SimpleUDPClient] = None
        self.logger = logging.getLogger(__name__)
        
        if self.enabled:
            try:
                self.client = udp_client.SimpleUDPClient(host, port)
                self.logger.info(f"OSC client initialized - sending to {host}:{port}")
            except Exception as e:
                self.logger.error(f"Failed to initialize OSC client: {e}")
                self.enabled = False
    
    def send_ball_position(self, position: Point2D, frame_width: int, frame_height: int) -> None:
        """Send ball position to Unreal Engine via OSC.
        
        Args:
            position: Ball position (x, y) in pixel coordinates
            frame_width: Video frame width for normalization
            frame_height: Video frame height for normalization
        """
        if not self.enabled or self.client is None:
            return
        
        x, y = position
        
        # Normalize coordinates to 0-1 range
        norm_x = x / frame_width
        norm_y = y / frame_height
        
        try:
            # Send raw pixel coordinates
            self.client.send_message("/ball/position/raw", [x, y])
            
            # Send normalized coordinates (0-1 range)
            self.client.send_message("/ball/position/normalized", [norm_x, norm_y])
            
            # Send centered coordinates (-1 to 1 range, useful for UE)
            centered_x = (x - frame_width / 2) / (frame_width / 2)
            centered_y = (y - frame_height / 2) / (frame_height / 2)
            self.client.send_message("/ball/position/centered", [centered_x, centered_y])
            
          #  self.logger.info(f"OSC: Sent ball position raw=({x}, {y}), normalized=({norm_x:.3f}, {norm_y:.3f})")
            
        except Exception as e:
            self.logger.error(f"Failed to send OSC message: {e}")
    
    def send_ball_lost(self) -> None:
        """Send message indicating ball tracking is lost."""
        if not self.enabled or self.client is None:
            return
        
        try:
            self.client.send_message("/ball/lost", [True])
            self.logger.info("OSC: Sent ball lost signal")
        except Exception as e:
            self.logger.error(f"Failed to send ball lost message: {e}")
    
    def send_tracking_info(self, fps: float, frame_count: int) -> None:
        """Send additional tracking information.
        
        Args:
            fps: Current frame rate
            frame_count: Current frame number
        """
        if not self.enabled or self.client is None:
            return
        
        try:
            self.client.send_message("/ball/tracking/fps", [fps])
            self.client.send_message("/ball/tracking/frame", [frame_count])
            self.logger.info(f"OSC: Sent tracking info - FPS: {fps:.1f}, Frame: {frame_count}")
        except Exception as e:
            self.logger.error(f"Failed to send tracking info: {e}")