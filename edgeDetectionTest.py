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

windowHelperOutput3 = [
    [
        "window 1", 1,
        0, 0, 
        2, 4
    ], 
    [
        "window 2", 0, 
        2, 1, 
        4, 3
    ]
]

#switch to test
windowHelper = windowHelperOutput1

#edge detection ouput (coordinates will be appended)
edgeDetectionOutput = []

# Create a grid representation with visual processing
def create_grid_with_visuals(window_data, grid_size=(5, 5)):
    """
    Create a grid representation where each cell contains the z-layer of the topmost window covering it.
    Shows visual progress step by step.
    """
    print("\n" + "="*60)
    print("CREATING GRID - STEP BY STEP VISUALIZATION")
    print("="*60)
    
    # Initialize grid with -1 (no window)
    grid = [[-1 for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    # Sort windows by z-layer (lower z = on top)
    sorted_windows = sorted(window_data, key=lambda x: x[1])
    
    print(f"\nInitial empty grid ({grid_size[0]}x{grid_size[1]}):")
    print_grid(grid)
    
    for i, window in enumerate(sorted_windows):
        name, z, x1, y1, x4, y4 = window
        
        # Skip ignored programs
        if name in ["", "Settings", "Windows Input Experience", "Program Manager"]:
            print(f"\n[Step {i+1}] Skipping ignored program: {name}")
            continue
        
        print(f"\n[Step {i+1}] Processing window: '{name}' (z-layer: {z})")
        print(f"  Coordinates: ({x1},{y1}) to ({x4},{y4})")
        
        # Show the window's area before applying
        window_mask = [["." for _ in range(grid_size[0])] for _ in range(grid_size[1])]
        for y in range(max(0, y1), min(grid_size[1], y4 + 1)):
            for x in range(max(0, x1), min(grid_size[0], x4 + 1)):
                window_mask[y][x] = str(z)
        
        print(f"  Window area (will fill with {z}):")
        for y in range(grid_size[1]):
            row = []
            for x in range(grid_size[0]):
                if window_mask[y][x] == str(z):
                    row.append(f"({z})")
                else:
                    row.append(" . ")
            print("  " + " ".join(row))
        
        # Fill grid cells covered by this window
        cells_filled = 0
        for y in range(max(0, y1), min(grid_size[1], y4 + 1)):
            for x in range(max(0, x1), min(grid_size[0], x4 + 1)):
                old_value = grid[y][x]
                grid[y][x] = z
                cells_filled += 1
        
        print(f"  Filled {cells_filled} cells with value {z}")
        print(f"  Grid after this window:")
        print_grid(grid)
    
    print("\n" + "="*60)
    print("FINAL GRID")
    print("="*60)
    print_grid(grid)
    
    return grid

def print_grid(grid, highlight_edges=None):
    """
    Print the grid with visual formatting.
    If highlight_edges is provided, mark edge positions.
    """
    height = len(grid)
    width = len(grid[0])
    
    # Print column headers
    col_headers = "   " + " ".join([f"{x:2}" for x in range(width)])
    print(col_headers)
    print("   " + "--" * width + "-")
    
    for y in range(height):
        row_str = f"{y:2}| "
        for x in range(width):
            value = grid[y][x]
            
            # Format cell based on edge highlighting
            if highlight_edges and (x, y) in highlight_edges:
                cell = f"*{value}*" if value != -1 else "*^*"
            else:
                cell = f" {value} " if value != -1 else " . "
            
            row_str += cell
        print(row_str)

def detect_horizontal_edges_with_visuals(grid):
    """
    Detect horizontal edges where there's a change in z-layer from one cell to the next.
    Shows visual progress of edge detection.
    """
    print("\n" + "="*60)
    print("DETECTING HORIZONTAL EDGES - STEP BY STEP")
    print("="*60)
    
    edges = []
    height = len(grid)
    width = len(grid[0])
    
    print(f"\nGrid dimensions: {width}x{height}")
    print_grid(grid)
    
    # Create a visual representation of edge detection
    edge_grid = [[" " for _ in range(width * 2 - 1)] for _ in range(height)]
    
    # Scan each row for horizontal edges
    for y in range(height):
        print(f"\n{'='*40}")
        print(f"Processing row y = {y}:")
        print("Current row values:", [grid[y][x] if grid[y][x] != -1 else "." for x in range(width)])
        
        current_segment = None
        current_z = None
        current_edge_start = None
        
        for x in range(width):
            # Visualize the current position
            if current_segment is not None:
                print(f"  x={x}: Current edge segment from x={current_edge_start}")
            else:
                print(f"  x={x}: No active edge segment")
            
            # Check if this cell is different from the cell to its right
            if x < width - 1:
                z_left = grid[y][x]
                z_right = grid[y][x + 1]
                
                # Display what we're comparing
                left_disp = z_left if z_left != -1 else "."
                right_disp = z_right if z_right != -1 else "."
                print(f"    Comparing cells [{x}]={left_disp} and [{x+1}]={right_disp}")
                
                # If there's a change, mark it as an edge
                if z_left != z_right:
                    print(f"    CHANGE DETECTED! Marking edge at x={x+0.5}")
                    
                    # Mark in edge grid (between cells)
                    edge_grid[y][x * 2 + 1] = "|"
                    
                    # Start new edge segment
                    if current_segment is None:
                        current_segment = x + 1  # Edge is between x and x+1
                        current_edge_start = x + 1
                        current_z = z_left if z_left != -1 else z_right
                        print(f"    Starting new edge segment at x={current_edge_start}")
                    
                    # Continue existing edge segment
                    else:
                        print(f"    Continuing existing edge segment (started at x={current_edge_start})")
                # No change, finish current edge segment if it exists
                elif current_segment is not None:
                    # Add the completed edge
                    if current_segment != x:  # Don't add zero-length edges
                        edges.append([current_segment, y, x, y])
                        print(f"    ✓ COMPLETED EDGE: ({current_segment},{y}) to ({x},{y})")
                        print(f"    Edge stored: {[current_segment, y, x, y]}")
                    else:
                        print(f"    Discarding zero-length edge at x={current_segment}")
                    current_segment = None
                    current_z = None
                    current_edge_start = None
            # End of row, finish current edge segment
            elif current_segment is not None:
                if current_segment != x:  # Don't add zero-length edges
                    edges.append([current_segment, y, x, y])
                    print(f"    ✓ END-OF-ROW EDGE: ({current_segment},{y}) to ({x},{y})")
                    print(f"    Edge stored: {[current_segment, y, x, y]}")
                else:
                    print(f"    Discarding zero-length edge at row end")
                current_segment = None
                current_z = None
                current_edge_start = None
        
        print(f"Row {y} complete. Found {len([e for e in edges if e[1] == y])} edges on this row.")
    
    # Display the edge grid
    print("\n" + "="*60)
    print("VISUAL EDGE REPRESENTATION")
    print("="*60)
    print("Legend: numbers=z-layers, |=edges, .=empty, spaces=no edge")
    print()
    
    # Print column headers
    col_headers = "   "
    for x in range(width):
        col_headers += f"{x} "
        if x < width - 1:
            col_headers += "  "
    print(col_headers)
    
    for y in range(height):
        # First line: grid values
        row1 = f"{y:2} "
        for x in range(width):
            value = grid[y][x]
            row1 += f"{value if value != -1 else '.'} "
            if x < width - 1:
                row1 += f"{edge_grid[y][x*2+1]} "
        print(row1)
        
        # Second line: edge indicators (if any vertical edges were being detected)
        # This is just for horizontal edges in this visualization
    
    print("\n" + "="*60)
    return edges

def extract_coordinates_and_detect_edges_with_visuals(window_data):
    """
    Main function to extract coordinates and detect edges from window data.
    Shows full visual processing.
    """
    print("\n" + "="*80)
    print("EDGE DETECTION PROCESS - FULL VISUALIZATION")
    print("="*80)
    
    # First, extract and show all windows
    print("\nINPUT WINDOW DATA:")
    print("-"*40)
    for i, window in enumerate(window_data):
        name, z, x1, y1, x4, y4 = window
        print(f"Window {i}: '{name}' (z={z}) from ({x1},{y1}) to ({x4},{y4})")
    
    # Create grid with visuals
    grid = create_grid_with_visuals(window_data)
    
    # Detect edges with visuals
    edges = detect_horizontal_edges_with_visuals(grid)
    
    # Display final results
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    if edges:
        print(f"\nFound {len(edges)} horizontal edge(s):")
        for i, edge in enumerate(edges):
            x1, y1, x2, y2 = edge
            print(f"  Edge {i}: ({x1},{y1}) to ({x2},{y2}) [length: {x2-x1}]")
        
        # Create a visual map with edges highlighted
        print("\nVisual map with edges marked:")
        height = len(grid)
        width = len(grid[0])
        
        # Create edge positions set
        edge_positions = set()
        for edge in edges:
            x1, y1, x2, y2 = edge
            for x in range(x1, x2 + 1):
                edge_positions.add((x, y1))
        
        print_grid(grid, highlight_edges=edge_positions)
    else:
        print("\nNo horizontal edges detected.")
    
    return edges

# Test function for different scenarios
def run_test(test_name, window_data, expected_edges=None):
    """
    Run a test with visual output.
    """
    print("\n" + "★"*80)
    print(f"RUNNING TEST: {test_name}")
    print("★"*80)
    
    edges = extract_coordinates_and_detect_edges_with_visuals(window_data)
    
    if expected_edges:
        print(f"\nExpected edges: {expected_edges}")
        print(f"Actual edges:   {edges}")
        
        if edges == expected_edges:
            print("✓ TEST PASSED!")
        else:
            print("✗ TEST FAILED!")
    
    return edges

# Run tests
print("="*80)
print("EDGE DETECTION TEST SUITE")
print("="*80)

# Test 1: Your first example
print("\n\nTEST 1: Basic overlapping windows (Model 1)")
edges1 = run_test(
    "Basic overlapping windows", 
    windowHelperOutput1,
    [[1, 3, 4, 3], [1, 4, 4, 4]]  # Expected edges
)

# Test 2: Your second example
print("\n\nTEST 2: Alternative arrangement")
edges2 = run_test(
    "Alternative arrangement", 
    windowHelperOutput2,
    [[3, 1, 4, 1], [3, 2, 4, 2], [3, 3, 4, 3], [3, 4, 4, 4]]  # Expected edges
)

# Test 3: Third example
print("\n\nTEST 3: Partial overlap")
edges3 = run_test(
    "Partial overlap", 
    windowHelperOutput3,
    []  # Expected edges (depends on your logic)
)

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print(f"Test 1 found {len(edges1)} edges: {edges1}")
print(f"Test 2 found {len(edges2)} edges: {edges2}")
print(f"Test 3 found {len(edges3)} edges: {edges3}")

# Function to use without visuals (for integration)
def process_window_data_simple(window_data):
    """
    Simple version without visuals for actual use.
    """
    # Create grid
    grid_size = (5, 5)  # Adjust based on your coordinate ranges
    grid = create_grid_with_visuals(window_data, grid_size)
    
    # Detect edges
    edges = detect_horizontal_edges_with_visuals(grid)
    
    return edges

# Example of how to use without all the visual output
def quick_process(window_data):
    """
    Quick processing without step-by-step visuals.
    """
    # Create grid
    grid_size = (5, 5)
    grid = [[-1 for _ in range(grid_size[0])] for _ in range(grid_size[1])]
    
    sorted_windows = sorted(window_data, key=lambda x: x[1])
    
    for window in sorted_windows:
        name, z, x1, y1, x4, y4 = window
        if name in ["", "Settings", "Windows Input Experience", "Program Manager"]:
            continue
        
        for y in range(max(0, y1), min(grid_size[1], y4 + 1)):
            for x in range(max(0, x1), min(grid_size[0], x4 + 1)):
                grid[y][x] = z
    
    # Detect edges
    edges = []
    height = len(grid)
    width = len(grid[0])
    
    for y in range(height):
        current_segment = None
        
        for x in range(width):
            if x < width - 1:
                z_left = grid[y][x]
                z_right = grid[y][x + 1]
                
                if z_left != z_right:
                    if current_segment is None:
                        current_segment = x + 1
                elif current_segment is not None:
                    if current_segment != x:
                        edges.append([current_segment, y, x, y])
                    current_segment = None
            elif current_segment is not None:
                if current_segment != x:
                    edges.append([current_segment, y, x, y])
                current_segment = None
    
    return edges

print("\n" + "="*80)
print("QUICK PROCESSING EXAMPLE")
print("="*80)
quick_edges = quick_process(windowHelperOutput1)
print(f"Quick processing result: {quick_edges}")