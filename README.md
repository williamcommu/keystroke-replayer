# Keystroke Replayer

### Core Functionality
- **Smart Text Input**: Large, syntax-highlighted text area with custom scrolling
- **Flexible Timing**: Adjustable delay (1-10 seconds) for seamless app switching
- **Variable Speed**: Configurable typing speed (1-200 chars/sec) for any application
- **Real-time Status**: Live feedback with icons showing current operation state

### Modern Interface
- **Dark Theme**: Eye-friendly dark color scheme with high contrast
- **Responsive Layout**: Fully resizable window that maintains proportions
- **Smooth Animations**: Fade effects for window open/close operations
- **Visual Hierarchy**: Clear section organization with modern spacing

### Safety & Reliability
- **Emergency Stop**: Move mouse to top-left corner for instant abort
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Threading**: Non-blocking operation keeps UI responsive during replay
- **Input Validation**: Smart validation of settings with helpful feedback

## System Requirements

- **Python 3.6+** with tkinter support
- **Windows/Mac/Linux** compatible
- **pyautogui** library for keystroke simulation
- **~10MB** disk space for installation

## Installation

1. Make sure you have Python installed on your system
2. Install the required dependency:
   ```
   pip install pyautogui
   ```
   
   Or use the requirements file:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python keystroke_replayer.py
   ```

2. The GUI will open with the following options:
   - **Text Area**: Paste or type the text you want to replay
   - **Delay**: Set how many seconds to wait before starting the replay (gives you time to switch to the target application)
   - **Typing Speed**: Set how fast the text should be typed (characters per second)

3. **To use the replayer**:
   - Paste or type your text in the large text area
   - Adjust the delay and typing speed settings as needed
   - Click "Start Replay"
   - Quickly switch to the target application where you want the text to appear
   - The text will automatically start typing after the delay period

4. **Emergency Stop**: If you need to stop the replay immediately, move your mouse cursor to the top-left corner of your screen

## Tips

- **Higher delay**: Use when you need more time to switch between applications
- **Lower typing speed**: Use for applications that are slow to respond or have input validation
- **Test first**: Try with simple text before using complex content
- **Target focus**: Make sure the target text field is focused before the replay starts

## Safety Features

- **Failsafe**: PyAutoGUI's failsafe feature is enabled - moving the mouse to the top-left corner will stop the replay
- **Threading**: The replay runs in a separate thread, so the GUI remains responsive
- **Error handling**: The application handles various error conditions gracefully

## Compatible Applications

This tool works with most applications that accept keyboard input, including:
- Legacy applications that don't support modern clipboard operations
- Virtual machines or remote desktop sessions
- Terminal applications
- Games with text input
- Web forms that block pasting

## Troubleshooting

- **"pyautogui is not installed"**: Install pyautogui using `pip install pyautogui`
- **Text not appearing**: Make sure the target application window is focused and the text cursor is in the correct field
- **Typing too fast**: Reduce the typing speed setting
- **Need more time to switch**: Increase the delay setting

## Requirements

- Python 3.6+
- pyautogui
- tkinter (usually included with Python)

## License

This script is provided as-is for educational and practical use.
