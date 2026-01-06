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

#placeholder for output retrieved from window_helper.exe
#   - All windows should/will be sorted from top down
windowHelperOutput1 = [
    [
        "window 1", 1,
        1, 1, 
        4, 4
    ], 
    [
        "window 2", 0,
        0, 0, 
        2, 2
    ],
]

windowHelperOutput2 = [
    [
        "window 1", 1,
        0, 0, 
        2, 2
    ], 
    [
        "window 2", 0, 
        1, 1, 
        4, 4
    ]
]

#switch to test
windowHelper = windowHelperOutput1

#edge detection ouput (coordinates will be appended)
edgeDetectionOutput = []

#MODEL 1
# - - - - -   -> 0 0 0 - -
# - - - - -   -> 0 0 0 1 1
# - - - - -   -> 0 0 0 1 1
# - - - - -   -> - 1 1 1 1
# - - - - -   -> - 1 1 1 1
#SHOULD OUTPUT in edgeDetectionOutput: (0,0)-(0,2)  (1,3)-(1,4) -> [[0,0,0,2], [1,3,1,4]]
#   - IF THE COORDINATE PAIRS EQUAL, DON'T APPEND IT TO edgeDetection

#MODEL 2
# - - - - -   -> 1 1 1 - -
# - - - - -   -> 1 0 0 0 0
# - - - - -   -> 1 0 0 0 0
# - - - - -   -> - 0 0 0 0
# - - - - -   -> - 0 0 0 0
#SHOULD OUTPUT in edgeDetectionOutput: (0,0)-(0,2)  (1,1)-(1,4) -> [[0,0,0,2], [1,1,1,4]]

#THE TOP LAYERS OF EACH BLOCK IS THE ONLY LAYER THAT SHOULD BE CONSIDERED

#IMPORTANT: JSON OUTPUT FORMAT
# [
#   ["Visual Studio Code", 0, 100, 50, 1500, 900],
#   ["Chrome", 1, 0, 0, 1920, 1080],
#   ["Desktop", 2, -1920, 0, 0, 1080]
# ]

# Create a grid representation
def create_grid(window_data, grid_size=(5, 5)):
    #Creates a stacked grid representation where each cell contains the ordered z-layors

    # Initialize grid with -1 (no window)
    grid = [[-1 for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Sort windows by z-layer (0 -> #)
    #   - list[0] = topmost layor
    sorted_windows = sorted(window_data, key=lambda x: x[1])
    
    for window in sorted_windows:
        name, z, x1, y1, x4, y4 = window
        
        # Skip ignored programs
        if name in ["", "Settings", "Windows Input Experience", "Program Manager"]:
            print(f"This program was rejected: {name}")
            continue
        else:
            print(f"This program was accepted: {name}")
        
        # Fill grid cells covered by this window
        for y in range(max(0, y1), min(grid_size[1], y4 + 1)):
            for x in range(max(0, x1), min(grid_size[0], x4 + 1)):
                grid[y][x] = z
    
    return grid

def detect_horizontal_edges(grid):
    # detects edges by differences in z-layor for further analysis

    edges = []
    height = len(grid)
    width = len(grid[0])
    
    # Scan each row for horizontal edges
    for y in range(height):
        current_segment = None
        current_z = None
        
        for x in range(width):
            # Check if this cell is different from the cell to its right
            if x < width - 1:
                z_left = grid[y][x]
                z_right = grid[y][x + 1]
                
                # If there's a change, mark it as an edge
                if z_left != z_right:
                    # Start new edge segment
                    if current_segment is None:
                        current_segment = x + 1  # Edge is between x and x+1
                        current_z = z_left if z_left != -1 else z_right
                    
                    # Continue existing edge segment
                    else:
                        # Edge continues at same y level
                        pass
                # No change, finish current edge segment if it exists
                elif current_segment is not None:
                    # Add the completed edge
                    if current_segment != x:  # Don't add zero-length edges
                        edges.append([current_segment, y, x, y])
                    current_segment = None
                    current_z = None
            # End of row, finish current edge segment
            elif current_segment is not None:
                if current_segment != x:  # Don't add zero-length edges
                    edges.append([current_segment, y, x, y])
                current_segment = None
                current_z = None
    
    return edges

#Main function that determines edges
def edgeDetection(window_data):
    # Programs to ignore
    ignored_programs = {"", "Settings", "Windows Input Experience", "Program Manager"}
    
    # First, create a grid representation
    grid = create_grid(window_data)
    
    # Detect edges
    edges = detect_horizontal_edges(grid)
    
    return edges

# Test with provided examples
print("Testing with windowHelperOutput1:")
edgeDetectionOutput = extract_coordinates_and_detect_edges(windowHelper)
print(f"\nEdge Detection Output: {edgeDetectionOutput}")
