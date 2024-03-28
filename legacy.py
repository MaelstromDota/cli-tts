import io
import logging
import os
import re
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import keyboard
import pygame
import simpleaudio as sa
import torch
import torchaudio
from num2words import num2words
from pydub import AudioSegment


logging.getLogger().setLevel(logging.ERROR)


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


class TTS():
	def __init__(self, speaker: str="kseniya", pitch: int=0):
		self._speaker = speaker
		self._pitch = pitch
		self._volume = 0
		self._voicemod = VoiceMod()
		torch._C._jit_set_profiling_mode(False)
		if not os.path.isfile("model.pt"):
			torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt', "model.pt")
		self._model = torch.package.PackageImporter("model.pt").load_pickle("tts_models", "model")
		self._model.to(torch.device("cuda"))
		torch.set_num_threads(4)
		pygame.mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")

		# for some reason works properly on 2nd tts
		# self.create_audio(text="тест")

	def play_audio(self, audio: io.BytesIO):
		pygame.mixer.music.load(audio)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy():
			time.sleep(0.1)

	def create_audio(self, text: str) -> io.BytesIO:
		tts_audio = self._model.apply_tts(text=text, speaker=self._speaker, sample_rate=48000, put_accent=True, put_yo=True)
		audio = io.BytesIO()
		torchaudio.save(audio, tts_audio.unsqueeze(0), sample_rate=48000, format="wav")
		audio.seek(0)
		return audio

	def format_numbers(self, text: str) -> str:
		return re.sub(r"\d+", lambda match: num2words(int(match.group()), lang="ru"), text)

	def say(self, text: str):
		modified_text = self.format_numbers(text)
		audio = self.create_audio(f"{modified_text}. ... ...")
		modified_audio = self._voicemod.pitch(audio, self._pitch)
		modified_audio = self._voicemod.volume(modified_audio, self._volume)
		return self.play_audio(modified_audio)

	def say_bind(self, text: str):
		modified_text = self.format_numbers(text)
		audio = self.create_audio(f"{modified_text}. ... ...")
		modified_audio = self._voicemod.pitch(audio, self._pitch)
		modified_audio = self._voicemod.volume(modified_audio, self._volume)
		sa.WaveObject.from_wave_file("blipSelect.wav").play()
		while not keyboard.is_pressed("n"):
			if keyboard.is_pressed("y"):
				return
			time.sleep(0.1)
		self.play_audio(modified_audio)
		return sa.WaveObject.from_wave_file("blipSelect.wav").play()


tts = TTS(speaker="baya", pitch=45)
tts._volume = -15

bind_say = input("Bind mode <0>/<1>: ")

while True:
	txt = input(">>> ")
	if re.search(r"^.p \-?\d+$", txt, re.IGNORECASE) is not None:
		tts._pitch = int(re.search(r"\-?\d+", txt).group())
	elif re.search(r"^.s .+$", txt, re.IGNORECASE) is not None:
		tts._speaker = txt[3:]
	elif re.search(r"^.v \-?\d+$", txt, re.IGNORECASE) is not None:
		tts._volume = int(re.search(r"\-?\d+", txt).group())
	elif re.search(r"^.b (0|1)$", txt, re.IGNORECASE) is not None:
		bind_say = re.search(r"0|1", txt).group()
	elif txt.startswith("!"):
		os.system(txt[1:])
	else:
		try:
			if bind_say == "1":
				tts.say_bind(txt)
			else:
				tts.say(txt)
		except ValueError as e:
			print(repr(e))
