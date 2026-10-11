extends AudioStreamPlayer

class_name SoundEffectPlayerScript;

var soundStarted: bool = false;
@export var sounds: Array[AudioStream];

func PlaySound() -> void:
	stream = sounds[randi_range(0, sounds.size())]
	#volume_db = vol
	#pitch_scale = variation
	playing = true
	soundStarted = true
	pass

func _process(delta: float) -> void:
	#if(soundStarted && !playing):
		#queue_free()
	pass
