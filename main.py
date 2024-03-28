import io
import logging
import os
import re
import traceback
import sys
from typing import TextIO

import keyboard
import simpleaudio as sa

logging.disable()

from util import VoiceMod, RUAccentModified, SSMLBuilder, TTS, Player

device = "cuda"
threads = 4

accentizer_model = "turbo"

speaker = "baya"
volume = -15
pitch = 45

play_interrupt_key = "pause"
play_key = "n"
destroy_audio_key = "y"
audio_ready_sound = "blipSelect.wav"
virtual_cable = "CABLE Input (VB-Audio Virtual Cable)"


ssml_builder = SSMLBuilder()

accentizer = RUAccentModified()
accentizer.load(omograph_model_size=accentizer_model, use_dictionary=False, device=device.upper())

tts = TTS(device=device.lower(), threads=threads)

voicemod = VoiceMod()

player = Player(interrupt_key=play_interrupt_key, virtual_cable=virtual_cable)


def prepare_audio(text: str) -> io.BytesIO:
	formatted_text = ssml_builder.build(f"{text} ;п500мс3п;")
	formatted_text = ssml_builder.format_numbers(formatted_text)
	formatted_text = accentizer.process_all_ssml(formatted_text)

	audio = tts.create_audio(ssml_text=formatted_text, speaker=speaker)
	if pitch != 0:
		audio = voicemod.pitch(audio, pitch)
	if volume != 0:
		audio = voicemod.volume(audio, volume)

	return audio

def say(text: str) -> bool:
	return player.play_audio(prepare_audio(text))

def play_sound(sound: str) -> sa.PlayObject | None:
	sound_path = os.path.normpath(sound)
	if not os.path.isfile(sound_path):
		return None
	return sa.WaveObject.from_wave_file(sound_path).play()

def say_bind(text: str) -> bool:
	audio = prepare_audio(text)
	if play_key:
		if audio_ready_sound:
			play_sound(audio_ready_sound)
		while event := keyboard.read_event():
			if event.event_type == keyboard.KEY_DOWN:
				if event.name == play_key:
					break
				elif event.name == destroy_audio_key:
					del audio
					return False
	played_audio = player.play_audio(audio)
	if audio_ready_sound:
		play_sound(audio_ready_sound)
	return played_audio

def print_exception(exc, /, value=traceback._sentinel, tb=traceback._sentinel, limit=None, file: TextIO=sys.stderr, chain=True) -> str:
	value, tb = traceback._parse_value_tb(exc, value, tb)
	info = ""
	for line in traceback.TracebackException(type(value), value, tb, limit=limit, compact=True).format(chain=chain):
		print(line, file=file, end="")
		info += line
	return info

logging.disable(logging.ERROR)

os.system("cls")

bind_say = input("Bind mode <0>/<1>: ")

while True:
	txt = input(">>> ")
	if re.search(r"^.p \-?\d+$", txt, re.IGNORECASE) is not None:
		pitch = int(re.search(r"\-?\d+", txt).group())
	elif re.search(r"^.s .+$", txt, re.IGNORECASE) is not None:
		speaker = txt[3:]
	elif re.search(r"^.v \-?\d+$", txt, re.IGNORECASE) is not None:
		volume = int(re.search(r"\-?\d+", txt).group())
	elif re.search(r"^.b (0|1)$", txt, re.IGNORECASE) is not None:
		bind_say = re.search(r"0|1", txt).group()
	elif txt.startswith("!"):
		os.system(txt[1:])
	else:
		try:
			if bind_say == "1":
				say_bind(txt)
			else:
				say(txt)
		except Exception:
			print_exception(*sys.exc_info())
