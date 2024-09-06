import re
import os

import ruaccent
from ruaccent.text_preprocessor import TextPreprocessor

from .ssml import SSMLBuilder


class RUAccentModified(ruaccent.RUAccent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.normalize = re.compile(r"[^a-zA-Z0-9\sа-яА-ЯёЁ—.,!?:;""''(){}[]«»„“”-+]") # NOTE: added +

	def _process_omographs(self, text):
		splitted_text = text

		founded_omographs = []
		texts = []
		hypotheses = []

		for i, word in enumerate(splitted_text):
			if "+" in word:
				continue
			variants = self.omographs.get(word)
			if variants:
				founded_omographs.append(
					{"word": word, "variants": variants, "position": i}
				)
				texts.append(splitted_text)
				hypotheses.append(variants)

		if len(founded_omographs) > 0:
			texts_batch = []
			hypotheses_batch = [val for sublist in hypotheses for val in sublist]

			for o, t in zip(founded_omographs, texts):
				position = o["position"]
				t_back = t[position]
				t[position] = ' <w>' + t[position] + '</w> '
				for _ in range(len(o["variants"])):
					texts_batch.append(self.delete_spaces_before_punc(" ".join(t.copy())))
				t[position] = t_back
			cls_batch = self.omograph_model.classify(texts_batch, hypotheses_batch)

			cls_index = 0
			for omograph in founded_omographs:
				position = omograph["position"]
				splitted_text[position] = cls_batch[cls_index]
				cls_index += 1

		return splitted_text

	@staticmethod
	def _search_processed_word_in_ssml(word: str, ssml_text: str) -> re.Match[str] | None:
		word = re.escape(word)
		formatted_word = word.replace("\\+", "")
		if match := re.search(rf"\b{formatted_word}\b", ssml_text, re.IGNORECASE):
			return match
		formatted_word = formatted_word.replace("ё", "е")
		if match := re.search(rf"\b{formatted_word}\b", ssml_text.replace("ё", "е"), re.IGNORECASE):
			return match
		return re.search(rf"\b{word}\b", ssml_text, re.IGNORECASE)

	def process_all_ssml(self, ssml_text: str) -> str:
		processed_text = self.process_all(SSMLBuilder.extract_only_text(ssml_text))
		processed_words = [word for word in TextPreprocessor.split_by_words(processed_text)[0] if "+" in word]

		if os.getenv("DEBUG", "0") == "1":
			print(f"[DEBUG]: {' '.join(processed_words)}")

		result = ssml_text
		for word in processed_words:
			if match := type(self)._search_processed_word_in_ssml(word, result):
				result = result[:match.start()] + word + result[match.end():]
			else:
				print(f"[RUAccentModified|process_all_ssml] no found word for \"{word}\" in \"{SSMLBuilder.extract_only_text(result)}\"!")

		return result
