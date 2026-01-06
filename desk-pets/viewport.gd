extends Node2D

var move_speed = 1
var direction = Vector2(1, 0) 
var velocity := Vector2.ZERO
var gravity := 0.4
var max_fall_speed := 10
@onready var window = get_window()
@onready var usable_rect = DisplayServer.screen_get_usable_rect()
@onready var target_y = usable_rect.end.y - window.size.y

@export var draggingDetector: Button
var beingDragged: bool = false
var dragDifference: Vector2

func _ready() -> void:

	
	window.position = Vector2i(0, usable_rect.position.y)

	velocity = Vector2.ZERO

func _process(_delta):
	
	var window = get_window()
	
	
	var usable_rect = DisplayServer.screen_get_usable_rect()
		
	if(!beingDragged):
		var move_vector = Vector2i(direction * move_speed)
		
		window.position += move_vector
		#window.position = lerp(Vector2(window.position), Vector2(DisplayServer.mouse_get_position()), move_speed * _delta) #mouse follow behaviour
		
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
		pass
	else:
		var mousePos = DisplayServer.mouse_get_position()
		window.position = mousePos + dragDifference
		pass

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			print("running")
			if event.pressed:
				beingDragged = true
				dragDifference = window.position - DisplayServer.mouse_get_position()
			else:
				beingDragged = false
