extends Node2D

<<<<<<< HEAD
var move_speed = 100
=======
var move_speed = 10

>>>>>>> aa2c1fbda3c6386232b696cc73c08a129aec6b1e
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

var bouncy: bool = true

func _ready() -> void:
	$pet.flip_h = true
	$pet/white_eye.flip_h = true
	$pet/pupil.flip_h = true
	#var window_id := window.get_window_id()
	DisplayServer.window_set_mouse_passthrough(PackedVector2Array())
	window.position = Vector2i(0, usable_rect.position.y)

	velocity = Vector2.ZERO
	$pet.play("normal")
	
func _process(_delta):
	
	window = get_window()
	usable_rect = DisplayServer.screen_get_usable_rect()
	
	
	
	if(!beingDragged):
		moveBackAndForth()
		#moveToMouse(_delta)
		
		changeDirectionsAtEdge()
		runInertia(_delta)
		
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
		$pet.flip_h = false
		$pet/white_eye.flip_h = false
		$pet/pupil.flip_h = false
	elif window.position.x < usable_rect.position.x:
		direction.x = 1
		$pet.flip_h = true
		$pet/white_eye.flip_h = true
		$pet/pupil.flip_h = true

func runGravity():
	velocity.y += gravity
	velocity.y = min(velocity.y, max_fall_speed)
	window.position += Vector2i(velocity)
	
	if window.position.y < usable_rect.position.y:
		dragInertia.y *= -1
		
		if(bouncy):
			dragInertia.y = abs(dragInertia.y)
		else:
			dragInertia.y = 0
		
		#window.position.y = usable_rect.position.y
	if window.position.y + window.size.y > usable_rect.end.y:
		velocity.y = 0;
		
		if(bouncy):
			dragInertia.y = abs(dragInertia.y) * -1
		else:
			dragInertia.y = 0
		
		window.position.y = usable_rect.end.y - window.size.y

func drag():
	var mousePos: Vector2 = DisplayServer.mouse_get_position()
	var currentPos: Vector2 = window.position
	window.position = mousePos + dragDifference
	dragInertia = Vector2(window.position) - currentPos
	velocity.y = 0
	
	if(dragInertia.x < 0):
		direction.x = abs(dragInertia.y) * -1
	if(dragInertia.x > 0):
		direction.x = abs(dragInertia.y)
	pass

func runInertia(_delta):
	dragInertia = dragInertia.lerp(Vector2(), _delta * move_speed);
	
	if(GetMagnitudeOf(dragInertia) < 0.05):
		dragInertia = Vector2()
		pass
	
	window.position += Vector2i(dragInertia)
	deleteInertiaAtEdges()
	pass

func deleteInertiaAtEdges():
	if window.position.x + window.size.x > usable_rect.end.x:
		if(bouncy):
			dragInertia.x *= -1;
		else:
			dragInertia.x = 0;
		
		window.position.x = usable_rect.end.x - window.size.x
	elif window.position.x < usable_rect.position.x:
		if(bouncy):
			dragInertia.x *= -1;
		else:
			dragInertia.x = 0;
		
		window.position.x = usable_rect.position.x;

func _input(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				beingDragged = true
				dragDifference = window.position - DisplayServer.mouse_get_position()
			else:
				beingDragged = false


func GetMagnitudeOf(value: Vector2):
	return sqrt((value.x * value.x) + (value.y * value.y))


	
