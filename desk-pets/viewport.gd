extends Node2D

var move_speed = 1
var direction = Vector2(1, 0) 
var velocity := Vector2.ZERO
var gravity := 0.4
var max_fall_speed := 10
@onready var window = get_window()
@onready var usable_rect = DisplayServer.screen_get_usable_rect()
@onready var target_y = usable_rect.end.y - window.size.y

var beingDragged: bool = false
var dragDifference: Vector2
var dragInertia: Vector2

func _ready() -> void:
	#var window_id := window.get_window_id()
	DisplayServer.window_set_mouse_passthrough(PackedVector2Array())
	window.position = Vector2i(0, usable_rect.position.y)

	velocity = Vector2.ZERO

func _process(_delta):
	
	window = get_window()
	usable_rect = DisplayServer.screen_get_usable_rect()
	
	
	
	if(!beingDragged):
		moveBackAndForth()
		#moveToMouse(_delta)
		
		runInertia(_delta)
		
		changeDirectionsAtEdge()
		runGravity()
		pass
	else:
		drag()
		pass

func moveToMouse(_delta):
	window.position = lerp(Vector2(window.position), Vector2(DisplayServer.mouse_get_position()), move_speed * _delta) #mouse follow behaviour

func moveBackAndForth():
	var move_vector = Vector2i(direction * move_speed)
	window.position += move_vector

func changeDirectionsAtEdge():
	if window.position.x + window.size.x > usable_rect.end.x:
		direction.x = -1
	elif window.position.x < usable_rect.position.x:
		direction.x = 1

func runGravity():
	velocity.y += gravity
	velocity.y = min(velocity.y, max_fall_speed)
	window.position += Vector2i(velocity)
	
	if window.position.y < usable_rect.position.y:
		#direction.y = -1
		dragInertia.y *= -1
	if window.position.y + window.size.y > usable_rect.end.y:
		velocity.y = 0;
		dragInertia.y *= -1
		window.position.y = usable_rect.end.y - window.size.y
	#if window.position.y >= target_y:
		#window.position.y = target_y
		#velocity.y = 0

func drag():
	var mousePos: Vector2 = DisplayServer.mouse_get_position()
	var currentPos: Vector2 = window.position
	window.position = mousePos + dragDifference
	dragInertia = Vector2(window.position) - currentPos
	velocity.y = 0
	
	if(dragInertia.x < 0):
		direction.x = -1
	if(dragInertia.x > 0):
		direction.x = 1
	pass

func runInertia(_delta):
	dragInertia = dragInertia.lerp(Vector2(), _delta * move_speed);
	window.position += Vector2i(dragInertia)
	deleteInertiaAtEdges()
	pass

func deleteInertiaAtEdges():
	if window.position.x + window.size.x > usable_rect.end.x:
		dragInertia.x *= -1
	elif window.position.x < usable_rect.position.x:
		dragInertia.x *= -1

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				beingDragged = true
				dragDifference = window.position - DisplayServer.mouse_get_position()
			else:
				beingDragged = false
