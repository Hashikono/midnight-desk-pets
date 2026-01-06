extends Node2D

@export var tempSquare: PackedScene

var squares: Array[Node2D] = []

func _ready() -> void:
	var output := []
	var exit_code = OS.execute(
		"edgeDetection.exe", # program
		[],                 # arguments
		output,             # stdout goes here
		true                # block until finished
		)

	if(exit_code != 0):
		print("Edge detection failed with code:", exit_code)
		return

	if(output.is_empty()):
		print("No output from helper")
		return

	var windows = JSON.parse_string(output[0])
	if windows == null:
		print("Failed to parse JSON")
		return
	
	
	#var ran: bool = false
	var godot_pos = DisplayServer.window_get_position()
	
	for w in windows:
		var rect := Rect2(w[0] - godot_pos.x, w[0] - godot_pos.y, w[0], w[0])
		
		print(rect)
		#var instance = tempSquare.instantiate()
		##add_sibling(instance);
		#instance.position = Vector2(w.x - godot_pos.x, w.y - godot_pos.y);
		#instance.scale.x = w.width
		#instance.scale.y = w.height
		
		#if(!ran):
			#print(w.x, ", ", w.y)
			#ran = true
		
		
		
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
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

	if(exit_code != 0):
		print("WindowHelper failed with code:", exit_code)
		return

	if(output.is_empty()):
		print("No output from helper")
		return

	var windows = JSON.parse_string(output[0])
	if windows == null:
		print("Failed to parse JSON")
		return
		
	print(output);
	
	
	#var ran: bool = false
	#var screenScale := DisplayServer.screen_get_scale()
	#var dpi := get_window().content_scale_factor
	#var godot_pos := DisplayServer.window_get_position()  # already logical pixels
#
	#var wasFirst := true
	#for w in windows:
		#if wasFirst:
			#wasFirst = false
			#continue  # skip first window if desired
#
		#var instance = tempSquare.instantiate()
		#add_sibling(instance)
#
		## Convert Windows physical → Godot logical, then relative to Godot window
		#var win_logical := Vector2(w.x, w.y) / dpi
		#instance.global_position = Vector2(win_logical.x - godot_pos.x, win_logical.y - godot_pos.y)
#
		#instance.scale = Vector2(0.1, 0.1)
		#squares.append(instance)
	pass
