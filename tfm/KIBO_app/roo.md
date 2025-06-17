# ⚠️ Sacred Project Context for Roo Code

This project follows strict architectural constraints. You MUST adhere to the following Sacred Objects:

## 🔱 Sacred Architecture
This app is a touchscreen-based educational story game for children (ages 6–10) that runs on a Raspberry Pi. It uses a serial-connected ESP32 for analog game input and output.

**Main Screens (Kivy):**
- SplashScreen → HomeScreen → LevelSelectionScreen → StoryScreen → MiniGameScreen → EndScreen

**Mini-Games:**
- Some are run on the ESP32 (e.g., memory, potentiometer matching).
- Some are run on the Raspberry Pi (e.g., drawing, lost & found).

## 📁 Sacred Project Folder
The file and folder structure must remain exactly as defined. You may not rename, move, or delete files without explicit permission. (God will destroy you if you do.)

Refer to `README.md` for the full folder layout.

## ⚙️ Sacred System Config
- Raspberry Pi 7” Touchscreen v1.1
- USB Serial to ESP32 (using `pyserial`)
- `speech_recognition` library for voice input
- VLC (via `python-vlc`) for MP3 audio playback

## 🧠 Rules for Roo
- Do not suggest changes to the Sacred Architecture without permission.
- Do not alter the folder or file names.
- Always assume touch input and serial I/O are active.
- Minigames are routed via `game_launcher.py` and may involve ESP32 commands.
- Audio playback must use VLC-compatible MP3 handling.

---

You are now a guardian of the Sacred Code. Proceed with reverence.
