import ctypes
import time
from ctypes import wintypes
import threading

# Constants for Windows API usage
SW_HIDE = 0
SW_SHOW = 5

# Get the handle to the user32.dll
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Define types for Windows API calls
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

# Global dictionary to store task states
task_states = {}

def is_window_visible(hwnd):
    """Check if the window is visible."""
    return user32.IsWindowVisible(hwnd)

def toggle_window_visibility(hwnd):
    """Toggle the visibility of the window."""
    if is_window_visible(hwnd):
        user32.ShowWindow(hwnd, SW_HIDE)
    else:
        user32.ShowWindow(hwnd, SW_SHOW)

def enum_window_callback(hwnd, lParam):
    """Callback function to enumerate windows."""
    if is_window_visible(hwnd):
        task_states[hwnd] = True
    else:
        task_states[hwnd] = False
    return True

def toggle_tasks():
    """Toggle visibility of all tasks."""
    for hwnd in task_states.keys():
        toggle_window_visibility(hwnd)

def main():
    """Main function to run TaskToggle."""
    # Enumerate all windows
    user32.EnumWindows(EnumWindowsProc(enum_window_callback), 0)
    
    # Set up a keyboard listener for toggling tasks
    print("Press 't' to toggle tasks or 'q' to quit.")

    while True:
        key_input = input().lower()
        if key_input == 't':
            toggle_tasks()
        elif key_input == 'q':
            print("Exiting TaskToggle.")
            break
        else:
            print("Invalid input. Press 't' to toggle tasks or 'q' to quit.")

if __name__ == "__main__":
    main()