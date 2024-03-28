import io

from pydub import AudioSegment


class VoiceMod():
	def __init__(self):
		pass

	def pitch(self, audio: io.BytesIO, pitch_shift: int) -> io.BytesIO:
		audio_segment = AudioSegment.from_file(audio, format="wav")
		modified_audio_segment = audio_segment._spawn(audio_segment.raw_data, overrides={"frame_rate": audio_segment.frame_rate + int(pitch_shift * 100)})
		modified_audio_segment = modified_audio_segment.set_frame_rate(audio_segment.frame_rate)
		modified_audio = io.BytesIO()
		modified_audio_segment.export(modified_audio, format="wav")
		modified_audio.seek(0)
		return modified_audio

	def volume(self, audio: io.BytesIO, volume_adjustment: float) -> io.BytesIO:
		audio_segment = AudioSegment.from_file(audio, format="wav")
		modified_audio_segment = audio_segment._spawn(audio_segment.raw_data)
		modified_audio_segment = modified_audio_segment + volume_adjustment
		modified_audio = io.BytesIO()
		modified_audio_segment.export(modified_audio, format="wav")
		modified_audio.seek(0)
		return modified_audio
