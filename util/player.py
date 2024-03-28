import io
import os
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import keyboard
import pygame


class Player():
	def __init__(self, interrupt_key: str | None=None, virtual_cable: str="CABLE Input (VB-Audio Virtual Cable)"):
		self.interrupt_key = interrupt_key
		pygame.mixer.init(devicename=virtual_cable)

	def play_audio(self, audio: io.BytesIO) -> bool:
		pygame.mixer.music.load(audio)
		pygame.mixer.music.play()
		interrupted = False
		while pygame.mixer.music.get_busy():
			if self.interrupt_key:
				if keyboard.is_pressed(self.interrupt_key):
					pygame.mixer.music.stop()
					interrupted = True
			time.sleep(0.1)
		return not interrupted
