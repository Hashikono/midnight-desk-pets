extends Node2D

@export var tempSquare: PackedScene

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
		var instance = tempSquare.instantiate()
		instance.add_sibling(self);
		instance.position = Vector2(w.x - godot_pos.x, w.y - godot_pos.y);
		instance.scale.x = w.width
		instance.scale.y = w.height
		
		#if(!ran):
			#print(w.x, ", ", w.y)
			#ran = true
		
		
		
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
