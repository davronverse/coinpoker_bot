import pyautogui
import time

# Example coordinates (replace with your specific x, y coordinates)
x, y = 100, 100

# Move the mouse to the specified coordinates
pyautogui.moveTo(x, y, duration=0)  # Optional: Move the mouse cursor visibly (can be omitted if not needed)

# Simulate a left mouse button click at the specified coordinates
pyautogui.mouseDown()
pyautogui.mouseUp()

# Optionally, pause briefly to simulate human-like interaction
time.sleep(1)
