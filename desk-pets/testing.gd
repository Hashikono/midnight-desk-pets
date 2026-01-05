extends Node


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	print("hello world")
	$Label.text = "nothing"
	$Label.modulate = Color.DARK_RED
	
