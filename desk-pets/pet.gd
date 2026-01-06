extends CharacterBody2D

var grabbed : bool = false

func _process(delta):
	#if grabbed:
		#var mouse_pos = get_global_mouse_position()
		#global_position = lerp(global_position, mouse_pos, 2)
	# Add the gravity.
	#if not is_on_floor():
		#velocity += get_gravity() * delta
	#move_and_slide()
	pass
func _input(event: InputEvent) -> void:
	#if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		#if event.pressed:
			#grabbed = true
		#else:
			#grabbed = false
	pass
