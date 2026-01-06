extends Node2D

var move_speed = 1
var direction = Vector2(1, 0) 

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var window = get_window()
	var usable_rect = DisplayServer.screen_get_usable_rect()
	var target_y = usable_rect.end.y - window.size.y
	
	window.position = Vector2i(0, target_y)

# Called every frame. 'delta' is the elapsed tim e since the previous frame.
func _process(_delta):
	var window = get_window()
	var move_vector = Vector2i(direction * move_speed)
	
	window.position += move_vector
	
	var usable_rect = DisplayServer.screen_get_usable_rect()
	
	if window.position.x + window.size.x > usable_rect.end.x:
		direction.x = -1
	elif window.position.x < usable_rect.position.x:
		direction.x = 1
