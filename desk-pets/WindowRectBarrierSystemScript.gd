extends Node

@export var tempSquare: PackedScene

func _ready() -> void:
	createLine(Vector2(5,60), Vector2(10, 70))
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


#simply pop in two opposite corners
func createLine(point1: Vector2, point2: Vector2):
	var middlePoint = (point2 + point1) / 2
	var instance = tempSquare.instantiate()
	add_child(instance)
	
	instance.global_position = middlePoint
	instance.scale = point2 - point1
	pass
