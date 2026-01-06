extends Node2D

var move_speed = 1
var direction = Vector2(1, 0) 
var velocity := Vector2.ZERO
var gravity := 0.4
var max_fall_speed := 10
@onready var window = get_window()
@onready var usable_rect = DisplayServer.screen_get_usable_rect()
@onready var target_y = usable_rect.end.y - window.size.y
# Called when the node enters the scene tree for the first time.
func _ready() -> void:

	
	window.position = Vector2i(0, usable_rect.position.y)

	velocity = Vector2.ZERO

func _process(_delta):
	
	var window = get_window()
	var move_vector = Vector2i(direction * move_speed)
	
	window.position += move_vector
	
	
	var usable_rect = DisplayServer.screen_get_usable_rect()
	
	if window.position.x + window.size.x > usable_rect.end.x:
		direction.x = -1
	elif window.position.x < usable_rect.position.x:
		direction.x = 1

	velocity.y += gravity
	velocity.y = min(velocity.y, max_fall_speed)
	window.position += Vector2i(velocity)

	if window.position.y >= target_y:
		window.position.y = target_y
		velocity.y = 0
