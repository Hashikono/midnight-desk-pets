import json
import win32gui
import win32api

#WINDOWS EXTRACTION/ENUMERATION

#grouping pixels for faster calculations
CELL_SIZE = 20

def get_desktop_size():
    width  = win32api.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
    height = win32api.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
    return width, height

def get_grid_size(screen_w, screen_h):
    cols = max(1, screen_w // CELL_SIZE)
    rows = max(1, screen_h // CELL_SIZE)
    return cols, rows

def get_windows():
    windows = []

    def enum_handler(hwnd, z):
        if not win32gui.IsWindowVisible(hwnd):
            return

        rect = win32gui.GetWindowRect(hwnd)
        x1, y1, x4, y4 = rect

        if x4 - x1 <= 0 or y4 - y1 <= 0:
            return

        title = win32gui.GetWindowText(hwnd)

        if title in ["", "Settings", "Windows Input Experience", "Program Manager"]:
            return

        windows.append([
            title,  # window name
            z,      # z-layer (0 = top)
            x1, y1, # top-left
            x4, y4  # bottom-right
        ])

    z = 0
    def callback(hwnd, _):
        nonlocal z
        enum_handler(hwnd, z)
        z += 1
        return True

    win32gui.EnumWindows(callback, None)
    return windows


#EDGE DETECTION STUFF...

def create_grid(window_data, grid_size):
    cols, rows = grid_size
    grid = [[-1 for _ in range(cols)] for _ in range(rows)]

    # Bottom → top so top windows overwrite
    sorted_windows = sorted(window_data, key=lambda x: x[1], reverse=True)

    for window in sorted_windows:
        _, z, x1, y1, x4, y4 = window

        gx1 = max(0, min(cols - 1, x1 // CELL_SIZE))
        gy1 = max(0, min(rows - 1, y1 // CELL_SIZE))
        gx4 = max(0, min(cols - 1, x4 // CELL_SIZE))
        gy4 = max(0, min(rows - 1, y4 // CELL_SIZE))

        for y in range(gy1, gy4 + 1):
            for x in range(gx1, gx4 + 1):
                grid[y][x] = z

    return grid



def detect_horizontal_top_edges(grid):
    edges = []
    height = len(grid)
    width = len(grid[0])

    is_top_edge = [[False for _ in range(width)] for _ in range(height)]

    for x in range(width):
        for y in range(height):
            current_z = grid[y][x]

            if current_z != -1:
                if y == 0:
                    is_top_edge[y][x] = True
                else:
                    above_z = grid[y - 1][x]
                    if above_z == -1 or above_z != current_z:
                        is_top_edge[y][x] = True

    for y in range(height):
        segment_start = None

        for x in range(width):
            if is_top_edge[y][x]:
                if segment_start is None:
                    segment_start = x
            else:
                if segment_start is not None and segment_start != x - 1:
                    edges.append([segment_start, y, x - 1, y])
                segment_start = None

        if segment_start is not None and segment_start != width - 1:
            edges.append([segment_start, y, width - 1, y])

    return edges


def edge_detection(window_data, grid_size):
    grid = create_grid(window_data, grid_size)
    return detect_horizontal_top_edges(grid)


#MAIN EXECUTION

def main():
    windows = get_windows()

    screen_w, screen_h = get_desktop_size()
    grid_size = get_grid_size(screen_w, screen_h)

    edges = edge_detection(windows, grid_size)

    output = {
        "screen": {
            "width": screen_w,
            "height": screen_h,
            "cell_size": CELL_SIZE,
            "cols": grid_size[0],
            "rows": grid_size[1]
        },
        "windows": windows,
        "edges": edges
    }

    print(json.dumps(output))

#why does this exist...
if __name__ == "__main__":
    main()
