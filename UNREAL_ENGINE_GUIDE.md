# Unreal Engine OSC Blueprint Guide
## Extracting and Using Ball Tracking X, Y Coordinates

This guide shows you how to receive OSC messages from the Python ball tracking system and use the coordinates to control objects in Unreal Engine.

---

## Part 1: Basic OSC Server Setup

### 1.1 Enable OSC Plugin
1. Go to **Edit → Plugins**
2. Search for "**OSC**"
3. Enable the **OSC** plugin
4. Restart Unreal Engine

### 1.2 Create OSC Server (Event BeginPlay)
In your Blueprint (Actor or Level Blueprint):

```
Event BeginPlay
  ↓
Create OSCServer
  - Receive IPAddress: 0.0.0.0  (or 127.0.0.1 for localhost only)
  - Port: 9999
  - Multicast Loopback: ✓ (checked)
  - Server Name: "oscserver"
  ↓
[Store the OSC Server reference for later use]
```

**Important Settings:**
- **Receive IPAddress**: 
  - Use `0.0.0.0` to listen on all network interfaces
  - Use `127.0.0.1` for localhost only (same machine)
- **Port**: Must match Python script (default: 9999)
- **Server Name**: Give it a unique name like "oscserver"

---

## Part 2: Binding to OSC Messages

### 2.1 Bind Event to Message Received

```
[OSC Server Reference]
  ↓
Bind Event to On Osc Message Received
  - Target: [OSC Server reference]
  - Event: [Create custom event - see below]
```

### 2.2 Create Custom Event Handler

Create a **Custom Event** called "**On Ball Position Received**" with these steps:

---

## Part 3: Extracting X and Y Coordinates

### Method A: Extract from /ball/position/raw (Pixel Coordinates)

```
Message Received Event
  ↓
┌─────────────────────────────────────────┐
│ 1. Check if this is the right message  │
└─────────────────────────────────────────┘
  ↓
Get OSC Message Address
  ↓
Convert OSC Address To String
  ↓
Branch (String equals "/ball/position/raw")
  ↓ True
┌─────────────────────────────────────────┐
│ 2. Extract the coordinate values       │
└─────────────────────────────────────────┘
  ↓
Get OSC Message Arguments
  ↓ (Returns Array of OSC Values)
  ↓
┌──────────────────────┬──────────────────────┐
│                      │                      │
Get (a copy) [Index 0] Get (a copy) [Index 1]
│ = X coordinate       │ = Y coordinate       │
│                      │                      │
Get Int Value          Get Int Value
│ = X (int)            │ = Y (int)            │
└──────────────────────┴──────────────────────┘
  ↓
[Use X and Y values to control your objects]
```

### Method B: Extract from /ball/position/normalized (0-1 Range)

**Best for UI elements or when you need percentage-based positioning**

```
Message Received Event
  ↓
Get OSC Message Address → Convert to String
  ↓
Branch (String equals "/ball/position/normalized")
  ↓ True
Get OSC Message Arguments
  ↓
┌──────────────────────┬──────────────────────┐
│                      │                      │
Get (a copy) [Index 0] Get (a copy) [Index 1]
│                      │                      │
Get Float Value        Get Float Value
│ = X (0.0 to 1.0)     │ = Y (0.0 to 1.0)     │
└──────────────────────┴──────────────────────┘
```

### Method C: Extract from /ball/position/centered (-1 to 1 Range)

**Best for 3D positioning or game mechanics**

```
Message Received Event
  ↓
Get OSC Message Address → Convert to String
  ↓
Branch (String equals "/ball/position/centered")
  ↓ True
Get OSC Message Arguments
  ↓
┌──────────────────────┬──────────────────────┐
│                      │                      │
Get (a copy) [Index 0] Get (a copy) [Index 1]
│                      │                      │
Get Float Value        Get Float Value
│ = X (-1.0 to 1.0)    │ = Y (-1.0 to 1.0)    │
└──────────────────────┴──────────────────────┘
```

---

## Part 4: Complete Blueprint Examples

### Example 1: Move a 3D Object Based on Ball Position

```
Message Received Event
  ↓
Get OSC Message Address → Convert to String
  ↓
Branch (equals "/ball/position/centered")
  ↓ True
Get OSC Message Arguments
  ↓
┌──────────────────┬──────────────────┐
│ X Coordinate     │ Y Coordinate     │
├──────────────────┼──────────────────┤
Get [0]            Get [1]
Get Float Value    Get Float Value
│ (Range: -1 to 1) │ (Range: -1 to 1) │
│                  │                  │
Multiply by 500    Multiply by 500
│ (Scale)          │ (Scale)          │
└────────┬─────────┴──────────────────┘
         ↓
Make Vector
  - X: [X value * scale]
  - Y: [Y value * scale]  
  - Z: 0 (or keep current Z)
         ↓
Set Actor Location
  - Target: [Your Ball Actor]
  - New Location: [Vector from above]
  - Sweep: False
```

### Example 2: Move a Widget/UI Element

```
Message Received Event
  ↓
Get OSC Message Address → Convert to String
  ↓
Branch (equals "/ball/position/normalized")
  ↓ True
Get OSC Message Arguments
  ↓
┌──────────────────┬──────────────────┐
│ X (normalized)   │ Y (normalized)   │
├──────────────────┼──────────────────┤
Get [0]            Get [1]
Get Float Value    Get Float Value
│                  │                  │
Multiply by 1920   Multiply by 1080
│ (Screen Width)   │ (Screen Height)  │
└────────┬─────────┴──────────────────┘
         ↓
Set Position in Viewport
  - Target: [Your Widget]
  - Position: [X, Y from above]
```

### Example 3: Smoothed Movement with Interpolation

```
Message Received Event
  ↓
[Extract X and Y as shown above]
  ↓
Store in variables:
  - Target X (Float)
  - Target Y (Float)

[Then in Event Tick:]

Event Tick
  ↓
Get Actor Location
  ↓
VInterp To (Vector Interpolation)
  - Current: [Current Location]
  - Target: [Make Vector from Target X, Target Y, Z]
  - Delta Time: [Get Delta Seconds]
  - Interp Speed: 5.0 (adjust for smoothness)
  ↓
Set Actor Location
  - New Location: [Interpolated Vector]
```

---

## Part 5: Handling Multiple OSC Message Types

### Complete Message Router

```
Message Received Event
  ↓
Get OSC Message Address → Convert to String → [Store in Variable: MessagePath]
  ↓
Switch on String: [MessagePath]

┌─────────────────────────────────────────────┐
│ Case: "/ball/position/centered"            │
│   → Extract X, Y → Move 3D Object          │
├─────────────────────────────────────────────┤
│ Case: "/ball/position/normalized"          │
│   → Extract X, Y → Update UI               │
├─────────────────────────────────────────────┤
│ Case: "/ball/lost"                         │
│   → Get [0] → Get Bool Value                │
│   → Hide ball or trigger "lost" animation  │
├─────────────────────────────────────────────┤
│ Case: "/ball/tracking/fps"                 │
│   → Get [0] → Get Float Value               │
│   → Display FPS on screen                  │
└─────────────────────────────────────────────┘
```

---

## Part 6: Coordinate System Conversions

### Python to Unreal Engine Coordinate Mapping

The Python system sends coordinates in different formats:

| OSC Message | Format | Range | Best Use Case |
|-------------|--------|-------|---------------|
| `/ball/position/raw` | Integers | 0 to resolution (e.g., 0-640, 0-480) | Direct pixel mapping |
| `/ball/position/normalized` | Floats | 0.0 to 1.0 | UI, percentages, screen-space |
| `/ball/position/centered` | Floats | -1.0 to 1.0 | 3D world space, game controls |

### Conversion Formulas in Unreal

**From Normalized (0-1) to World Space:**
```
X_World = (X_Normalized - 0.5) * WorldScale * 2
Y_World = (Y_Normalized - 0.5) * WorldScale * 2

Example: If WorldScale = 1000
- Normalized 0.5, 0.5 → World 0, 0 (center)
- Normalized 1.0, 1.0 → World 1000, 1000 (top-right)
- Normalized 0.0, 0.0 → World -1000, -1000 (bottom-left)
```

**From Centered (-1 to 1) to World Space:**
```
X_World = X_Centered * WorldScale
Y_World = Y_Centered * WorldScale

Example: If WorldScale = 500
- Centered 0, 0 → World 0, 0 (center)
- Centered 1, 1 → World 500, 500
- Centered -1, -1 → World -500, -500
```

---

## Part 7: Debugging Tips

### 7.1 Print Debug Information

Add these after extracting coordinates:

```
Print String
  - In String: "Ball X: {X} Y: {Y}"
  - Text Color: Green
  - Duration: 0.0
  - Key: "BallPos"
```

### 7.2 Visual Debug

```
Draw Debug Sphere
  - Center: [Ball Position Vector]
  - Radius: 50
  - Color: Red
  - Duration: 0.1
```

### 7.3 Check Message Reception

```
Message Received Event
  ↓
Print String: "OSC Message Received!"
  ↓
Get OSC Message Address → Convert to String → Print String
  ↓
Get OSC Message Arguments → Length → Print String ("Arg Count: {}")
```

---

## Part 8: Performance Optimization

### 8.1 Reduce Update Frequency

If getting too many messages, add a timer:

```
Message Received Event
  ↓
[Store coordinates in variables]
  ↓
Branch: Is Timer Active?
  False ↓
    Set Timer by Function Name
      - Function: "UpdateBallPosition"
      - Time: 0.033 (30 FPS update rate)
      - Looping: False
```

### 8.2 Use Event-Driven Updates

Only update when position changes significantly:

```
[New X, Y values received]
  ↓
Distance (Vector)
  - A: [Current Position]
  - B: [New Position]
  ↓
Branch: Distance > Threshold (e.g., 10.0)
  True ↓
    Update Position
```

---

## Part 9: Common Issues and Solutions

### Issue 1: Not Receiving Messages
**Solution:**
- Check IPAddress is `0.0.0.0` or `127.0.0.1`
- Verify port matches Python (9999)
- Check Windows Firewall settings
- Run Python test: `uv run python simple_osc_test.py --port 9999`

### Issue 2: Getting Address but Not Values
**Solution:**
- Make sure to use "Get OSC Message Arguments"
- Use correct index (0 for X, 1 for Y)
- Use "Get Float Value" or "Get Int Value" based on message type

### Issue 3: Jittery Movement
**Solution:**
- Use VInterp To for smooth interpolation
- Implement smoothing with previous values
- Reduce update frequency

### Issue 4: Coordinates Seem Inverted
**Solution:**
- Y-axis might be inverted (screen vs. world space)
- Multiply Y by -1 if needed
- Adjust coordinate mapping formula

---

## Part 10: Quick Start Checklist

- [ ] Enable OSC plugin in Unreal Engine
- [ ] Create OSC Server node with port 9999
- [ ] Bind to "On Osc Message Received" event
- [ ] Add "Get OSC Message Address" node
- [ ] Add "Get OSC Message Arguments" node
- [ ] Extract coordinates using "Get (a copy)" with index 0 and 1
- [ ] Use "Get Float Value" or "Get Int Value" on each argument
- [ ] Apply coordinates to your actor/object
- [ ] Test with: `uv run tracking --show-masks`

---

## Python Commands Reference

```powershell
# Start ball tracking (sends OSC to port 9999)
uv run tracking

# Start with custom port
uv run tracking --osc-port 8000

# Send to different IP address
uv run tracking --osc-host 192.168.1.100

# Disable OSC
uv run tracking --disable-osc

# Test OSC reception
uv run python simple_osc_test.py --port 9999
```

---

## Need Help?

If you're still having issues:

1. Run the Python OSC test receiver to verify messages are being sent
2. Add Print String nodes to see what data is being received
3. Check the Output Log in Unreal Engine for errors
4. Verify the OSC plugin is properly enabled

---

**Created for Ball Tracking OSC Integration - November 2025**
