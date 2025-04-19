# 🖐️ Hand Gesture Mouse Control (MediaPipe + OpenCV)

This project allows you to control your mouse cursor using just your **hand gestures** in front of a webcam — no physical mouse required! Leveraging the power of **MediaPipe**, **OpenCV**, and **PyAutoGUI**, this system provides smooth real-time cursor control and gesture-based clicking.

It’s lightweight, efficient, and an exciting example of what can be done with modern computer vision and hand tracking libraries.

---

## 🧠 How It Works

Using a webcam and [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands), the system detects 21 hand landmarks per frame and interprets gestures based on finger positions and distances between fingertips. The recognized gestures are mapped to standard mouse actions:

- **Mouse Movement**: Move your index finger to move the cursor.
- **Left Click**: Pinch your thumb and index finger.
- **Right Click**: Pinch your index and middle fingers.

All processing is optimized for low latency and high responsiveness, even on lower-end systems.

---

## 🎮 Features

- 🖱️ Real-time mouse movement with hand gestures.
- 🤏 Left click gesture (thumb + index pinch).
- 🤌 Right click gesture (index + middle pinch).
- 💡 Adjustable gesture detection thresholds.
- ⚡ Highly responsive and lightweight on CPU.
- 🚫 Scroll gesture removed for better performance.

---

## 🧰 Requirements

Python 3.7 or later is recommended. Install dependencies using the included `requirements.txt`.

### 📦 Install dependencies

```bash
pip install -r requirements.txt
