import json
import win32gui

windows = []

def enum_handler(hwnd, z):
    if not win32gui.IsWindowVisible(hwnd):
        return

    rect = win32gui.GetWindowRect(hwnd)
    x1, y1, x4, y4 = rect

    if x4 - x1 <= 0 or y4 - y1 <= 0:
        return

    title = win32gui.GetWindowText(hwnd)

    windows.append([
        title,   # window name
        z,       # z layer (0 = top)
        x1, y1,  # top-left
        x4, y4   # bottom-right
    ])

# EnumWindows runs top → bottom
z = 0
def callback(hwnd, _):
    global z
    enum_handler(hwnd, z)
    z += 1
    return True

win32gui.EnumWindows(callback, None)

# Output as JSON (Godot-friendly)
print(json.dumps(windows))