# This is merely a model of the edge detection stuff for the sprite's usable platforms and will be
# translated into GDscript once everything is finalized

#Input from window_helper.exe (or whatever we're using)
#WINDOW HELPER OUT: [window name, z layer #, x1, y1, x4, y4] -> coordinates will be transcribed to be vector2()
#   - z layer # : top layer will be 0 and bottom layer will be the greatest number
#   - we only need two coordinates for the corners of the rectanglular window (see figure below)
#EDGE DETECTION OUT: [x1, y1, x2, y2] -> length/4 = how many horiontal edges there are

# 1️⃣---------------2️⃣
# |                  |
# |                  |
# |                  |
# 3️⃣---------------4️⃣

#MODEL 2
# - - - - -   -> 0 0 0 - -
# - - - - -   -> 0 0 0 1 1
# - - - - -   -> 0 0 0 1 1
# - - - - -   -> - 1 1 1 1
# - - - - -   -> - 1 1 1 1
#SHOULD OUTPUT in edgeDetectionOutput: (0,0)-(2,0)  (3,1)-(4,1) -> [[0,0,2,0], [3,1,4,1]]
#   - IF THE COORDINATE PAIRS EQUAL, DON'T APPEND IT TO edgeDetection

#MODEL 1
# - - - - -   -> 1 1 1 - -
# - - - - -   -> 1 0 0 0 0
# - - - - -   -> 1 0 0 0 0
# - - - - -   -> - 0 0 0 0
# - - - - -   -> - 0 0 0 0
#SHOULD OUTPUT in edgeDetectionOutput: (0,0)-(2,0)  (1,1)-(4,1) -> [[0,0,2,0], [1,1,4,1]]

#THE TOP LAYERS OF EACH BLOCK IS THE ONLY LAYER THAT SHOULD BE CONSIDERED

#IMPORTANT: JSON OUTPUT FORMAT
# [
#   ["Visual Studio Code", 0, 100, 50, 1500, 900],
#   ["Chrome", 1, 0, 0, 1920, 1080],
#   ["Desktop", 2, -1920, 0, 0, 1080]
# ]

#placeholder for output retrieved from window_helper.exe
#   - All windows should/will be sorted from top down
windowHelperOutput1 = [
    ["window 1", 0, 1, 1, 4, 4],
    ["window 2", 1, 0, 0, 2, 2],
]

windowHelperOutput2 = [
    ["window 1", 0, 0, 0, 2, 2],
    ["window 2", 1, 1, 1, 4, 4],
]

#switch to test
windowHelper = windowHelperOutput1

#edge detection ouput (coordinates will be appended)
edgeDetectionOutput = []


def create_grid(window_data, grid_size=(5, 5)):
    """Create grid where each cell has the z-layer of the topmost window."""
    grid = [[-1 for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Process windows from BOTTOM to TOP (highest z first, lowest z last)
    # z=1 (bottom) gets painted first, z=0 (top) paints over it
    sorted_windows = sorted(window_data, key=lambda x: x[1], reverse=True)
    
    for window in sorted_windows:
        name, z, x1, y1, x4, y4 = window
        
        if name in ["", "Settings", "Windows Input Experience", "Program Manager"]:
            print(f"Rejected: {name}")
            continue
        else:
            print(f"Accepted: {name} (z={z})")
        
        for y in range(max(0, y1), min(grid_size[1], y4 + 1)):
            for x in range(max(0, x1), min(grid_size[0], x4 + 1)):
                grid[y][x] = z  # Always overwrite - that's correct for bottom-to-top
    
    return grid

def detect_horizontal_top_edges(grid):
    """Find only the TOP edges of platform blocks - only the highest cell in each vertical segment."""
    edges = []
    height = len(grid)
    width = len(grid[0])
    
    print("\nGrid:")
    for y in range(height):
        row = [str(grid[y][x]) if grid[y][x] != -1 else "-" for x in range(width)]
        print(f"  {y}: {' '.join(row)}")
    
    # Create a mask of "is this a top edge?"
    is_top_edge = [[False for _ in range(width)] for _ in range(height)]
    
    for x in range(width):
        for y in range(height):
            current_z = grid[y][x]
            
            # Cell is occupied
            if current_z != -1:
                # Check cell above
                if y == 0:
                    # Top of grid is always a top edge
                    is_top_edge[y][x] = True
                else:
                    above_z = grid[y-1][x]
                    # It's a top edge ONLY if above is empty (not just different!)
                    # Because if above has same z, it's part of same vertical platform
                    if above_z == -1:
                        is_top_edge[y][x] = True
                    # Actually wait, if above has DIFFERENT z, current cell IS a top edge
                    # for its own layer! Example: z=0 above z=1
                    elif above_z != current_z:
                        is_top_edge[y][x] = True
    
    print("\nTop edge mask (T = top edge):")
    for y in range(height):
        row = []
        for x in range(width):
            row.append("T" if is_top_edge[y][x] else ".")
        print(f"  {y}: {' '.join(row)}")
    
    # Group consecutive top edges horizontally
    for y in range(height):
        segment_start = None
        
        for x in range(width):
            if is_top_edge[y][x]:
                if segment_start is None:
                    segment_start = x
            else:
                if segment_start is not None:
                    # End the segment
                    if segment_start != x - 1:  # Only if length > 0
                        edges.append([segment_start, y, x - 1, y])
                    segment_start = None
        
        # Handle segment at row end
        if segment_start is not None:
            if segment_start != width - 1:  # Only if length > 0
                edges.append([segment_start, y, width - 1, y])
    
    return edges

def edgeDetection(window_data):
    """Main edge detection function."""
    grid = create_grid(window_data, (5, 5))
    return detect_horizontal_top_edges(grid)


# Test
print("=" * 50)
print("Testing windowHelperOutput1 (should give [[0,0,2,0], [3,1,4,1]]):")
result1 = edgeDetection(windowHelperOutput1)
print(f"Result: {result1}")

print("\n" + "=" * 50)
print("Testing windowHelperOutput2 (should give [[0,0,2,0], [1,1,4,1]]):")
result2 = edgeDetection(windowHelperOutput2)
print(f"Result: {result2}")

print("\n" + "=" * 50)
print("Summary:")
print(f"windowHelperOutput1: {result1}")
print(f"windowHelperOutput2: {result2}")