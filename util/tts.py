import io
import os
from typing import overload

import torch
import torchaudio


class TTS():
	def __init__(self, model: str="https://models.silero.ai/models/tts/ru/v3_1_ru.pt", device: str="cpu", threads: int=4):
		torch._C._jit_set_profiling_mode(False)
		model_name = model.split("/")[-1]
		if not os.path.isfile(model_name):
			torch.hub.download_url_to_file(model, model_name)
		self._model = torch.package.PackageImporter(model_name).load_pickle("tts_models", "model")
		self._model.to(torch.device(device))
		torch.set_num_threads(threads)

	def apply_tts(self, **kwargs) -> io.BytesIO:
		tts_audio = self._model.apply_tts(**kwargs)
		audio = io.BytesIO()
		torchaudio.save(audio, tts_audio.unsqueeze(0), sample_rate=48000, format="wav")
		audio.seek(0)
		return audio

	@overload
	def create_audio(self, text: str, speaker: str) -> io.BytesIO:
		...

	@overload
	def create_audio(self, ssml_text: str, speaker: str) -> io.BytesIO:
		...

	def create_audio(self, text: str | None=None, ssml_text: str | None=None, speaker: str="") -> io.BytesIO:
		if text is None and ssml_text is None:
			raise ValueError("text or ssml_text must be specified")
		if not speaker:
			raise ValueError("speaker must be specified")
		if ssml_text is not None:
			return self.apply_tts(ssml_text=ssml_text, speaker=speaker, sample_rate=48000, put_accent=True, put_yo=True)
		return self.apply_tts(text=text, speaker=speaker, sample_rate=48000, put_accent=True, put_yo=True)
