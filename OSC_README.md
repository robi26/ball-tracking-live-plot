# Ball Tracking with OSC Integration

This project now includes OSC (Open Sound Control) support to send real-time ball coordinates to Unreal Engine or other applications.

## OSC Messages Sent

The application sends the following OSC messages when a ball is detected:

### Ball Position Messages
- `/ball/position/raw` - Raw pixel coordinates `[x, y]`
- `/ball/position/normalized` - Normalized coordinates (0-1 range) `[x, y]`
- `/ball/position/centered` - Centered coordinates (-1 to 1 range) `[x, y]`

### Ball Tracking Status
- `/ball/lost` - Sent when ball tracking is lost `[true]`

### Tracking Information
- `/ball/tracking/fps` - Current frame rate `[fps_value]`
- `/ball/tracking/frame` - Current frame number `[frame_count]`

## Usage

### Basic Usage with OSC
```bash
python -m ball_tracking.tracking --osc-host 127.0.0.1 --osc-port 8000
```

### Command Line Options
- `--osc-host` - OSC server host (default: 127.0.0.1)
- `--osc-port` - OSC server port (default: 8000)
- `--disable-osc` - Disable OSC communication entirely

### Testing OSC Communication

1. **Start the test OSC server** (in a separate terminal):
```bash
python test_osc_server.py
```

2. **Run ball tracking** (in another terminal):
```bash
python -m ball_tracking.tracking
```

The test server will display received OSC messages in real-time.

## Unreal Engine Integration

### Setup in Unreal Engine

1. **Enable OSC Plugin**:
   - Go to Edit → Plugins
   - Search for "OSC" 
   - Enable the OSC plugin
   - Restart Unreal Engine

2. **Create OSC Server**:
   - In your Blueprint or C++ code, create an OSC Server component
   - Set the listening port (default: 8000)
   - Bind to the appropriate OSC addresses

### Example Blueprint Setup

1. **Create OSC Server Component** in your Actor/GameMode
2. **Bind OSC Events** to handle incoming messages:

```
Event: /ball/position/normalized
Parameters: Float X, Float Y
Action: Update ball position in 3D space
```

### Coordinate Systems

- **Raw**: Direct pixel coordinates from camera feed
- **Normalized** (0-1): Best for UI elements, percentages
- **Centered** (-1 to 1): Best for 3D positioning, commonly used in game engines

Example conversion for Unreal Engine world coordinates:
```
World_X = Centered_X * World_Width_Scale
World_Y = Centered_Y * World_Height_Scale
```

### Sample Unreal Engine Blueprint Events

```
On OSC Message "/ball/position/centered":
  - Get Float Array (X, Y)
  - Multiply X by desired world scale
  - Multiply Y by desired world scale  
  - Set Actor Location

On OSC Message "/ball/lost":
  - Hide ball actor or trigger lost ball logic
```

## Troubleshooting

1. **No OSC messages received**:
   - Check firewall settings
   - Verify host and port settings
   - Ensure both applications are running

2. **Performance issues**:
   - Use `--disable-osc` to test without OSC
   - Reduce frame rate if needed
   - Consider using only normalized or centered coordinates

3. **Connection issues**:
   - Test with the provided test server first
   - Check network connectivity
   - Verify Unreal Engine OSC plugin is enabled