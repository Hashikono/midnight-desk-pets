extends Node2D

@export var betterTestSquare = preload("res://Scenes/betterTestSquare.tscn")

var squares: Array[Node2D] = []

func _ready() -> void:
	process_window_data()
	
func process_window_data() -> void:
	# Clear existing squares
	while(squares.size() > 0):
		squares[0].queue_free()
		squares.remove_at(0)
	
	var output := []
	var exit_code = OS.execute(
		"edgeDetection.exe", # program
		[],                 # arguments
		output,             # stdout goes here
		true                # block until finished
	)

	if exit_code != 0:
		print("Edge detection failed with code:", exit_code)
		return

	if output.is_empty():
		print("No output from helper")
		return

	# Parse the JSON string
	var json_result = JSON.parse_string(output[0])
	if json_result == null:
		print("Failed to parse JSON")
		return
	
	print("Raw JSON output: ", output[0])
	print("Parsed JSON: ", json_result)
	
	# Access screen information
	if json_result.has("screen"):
		var screen_data = json_result["screen"]
		print("Screen Info:")
		print("  Position: (", screen_data["vx"], ", ", screen_data["vy"], ")")
		print("  Size: ", screen_data["width"], "x", screen_data["height"])
		print("  Cell Size: ", screen_data["cell_size"])
		print("  Grid: ", screen_data["cols"], "x", screen_data["rows"])
	
	# Process windows
	if json_result.has("windows"):
		var windows_list = json_result["windows"]
		print("\nProcessing Windows:")
		
		# Skip the first element if it's the header ["Window name", "z-layer", "x1", "y1", "x4", "y4"]
		var start_index = 0
		if windows_list.size() > 0 and windows_list[0][0] == "Window name":
			start_index = 1
			print("Skipping header row")
		
		var godot_window_pos = DisplayServer.window_get_position()
		
		for i in range(start_index, windows_list.size()):
			var window_data = windows_list[i]
			
			# Extract window coordinates
			var window_name = window_data[0]
			#var z_layer = window_data[1]
			var x1 = window_data[2] as int
			var y1 = window_data[3] as int
			var x4 = window_data[4] as int
			var y4 = window_data[5] as int
			
			print("\nWindow ", i - start_index, ": ", window_name)
			print("  Position: (", x1, ", ", y1, ") to (", x4, ", ", y4, ")")
			print("  Size: ", x4 - x1, " x ", y4 - y1)
			
			# Create a visual representation
			var instance = betterTestSquare.instantiate()
			add_child(instance)
			
			# Calculate position and size for Godot
			# Convert from global screen coordinates to relative Godot window coordinates
			var center_x = (x1 + x4) / 2.0
			var center_y = (y1 + y4) / 2.0
			var width = x4 - x1
			
			# SETTED THIS TO CONSTANT CHANGE LATER MAYBE
			var height = 3
			
			# Adjust for Godot window position
			instance.position = Vector2(center_x - godot_window_pos.x, center_y - godot_window_pos.y)
			
			# Scale the square to match window size (adjust scaling factor as needed)
			var scale_factor = 0.01  # Adjust this based on your scene scale
			instance.scale = Vector2(width * scale_factor, height * scale_factor)
			
			# Store reference for cleanup
			squares.append(instance)
	
	# Process edges
	if json_result.has("edges"):
		var edges_list = json_result["edges"]
		print("\nProcessing Edges:")
		
		var start_edge_index = 0
		
		for i in range(start_edge_index, edges_list.size()):
			var edge_data = edges_list[i]
			
			var x1 = edge_data[0] as int
			var y1 = edge_data[1] as int
			var x2 = edge_data[2] as int
			var y2 = edge_data[3] as int
			
			print("Edge ", i - start_edge_index, ": (", x1, ", ", y1, ") to (", x2, ", ", y2, ")")
			
			# You could create visual representations for edges here too
			# For example, draw lines between these points

#func _process(delta: float) -> void:
	# If you want to update in real-time, uncomment this line:
	# process_window_data()
	# pass
	
func createLine(point1: Vector2, point2: Vector2):
	var middlePoint = (point2 + point1) / 2
	var instance = betterTestSquare.instantiate()
	add_child(instance)
	
	instance.global_position = middlePoint
	instance.scale = point2 - point1
	pass
