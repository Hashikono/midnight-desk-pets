extends Node2D


# Called when the node enters the scene tree for the first time.
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

	for w in windows:
		var rect := Rect2(w.x, w.y, w.width, w.height)
		print(rect)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
