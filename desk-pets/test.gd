extends Node2D

@export var tempSquare: PackedScene

var squares: Array[Node2D] = []

func _ready() -> void:
	var output := []
	var exit_code = OS.execute(
		"WindowHelper.exe", # program
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
	
	
	#var ran: bool = false
	var godot_pos = DisplayServer.window_get_position()
	
	for w in windows:
		var rect := Rect2(w.x - godot_pos.x, w.y - godot_pos.y, w.width, w.height)
		
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
		"WindowHelper.exe", # program
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
	
	
	#var ran: bool = false
	#var screenScale := DisplayServer.screen_get_scale()
	var screenScale := get_window().content_scale_factor
	var godot_pos: Vector2 = DisplayServer.window_get_position() * screenScale;
	
	#godot_pos *= screenScale;
	
	var wasFirst: bool = true
	for w in windows:
		#var rect := Rect2(w.x - godot_pos.x, w.y - godot_pos.y, w.width, w.height)
		
		if(!wasFirst):
			var instance = tempSquare.instantiate()
			add_sibling(instance);
			
			var newPos = Vector2(w.x, w.y)
			var localized = (Vector2(newPos.x - godot_pos.x, newPos.y - godot_pos.y) / screenScale)
			instance.global_position = get_viewport().get_canvas_transform().affine_inverse() * localized;
			instance.scale.x = 0.1
			instance.scale.y = 0.1
			squares.append(instance);
			#print("running")
		wasFirst = false
	pass
