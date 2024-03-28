import re

import ruaccent

from .ssml import SSMLBuilder


class RUAccentModified(ruaccent.RUAccent):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.normalize = re.compile(r"[^a-zA-Z0-9\sа-яА-ЯёЁ.,!?:;""''(){}[]«»„“”-+]") # NOTE: added +

	@staticmethod
	def has_word_accent(word: str) -> bool:
		return re.search(r"\+([аеёиоуыэюя])", word, re.IGNORECASE) is not None

	def _process_omographs(self, text, sentence):
		splitted_text = text

		founded_omographs = []
		texts = []
		hypotheses = []

		for i, word in enumerate(splitted_text):
			if type(self).has_word_accent(word):
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
				#print(splitted_text)
				#print(cls_batch)
				#print(cls_index)
				splitted_text[position] = cls_batch[cls_index]
				cls_index += 1

		return splitted_text

	def _process_accent(self, text, stress_usages):
		splitted_text = text

		for i, word in enumerate(splitted_text):
			if stress_usages[i] == "STRESS":
				if type(self).has_word_accent(word):
					continue
				stressed_word = self.accents.get(word, word)
				if stressed_word == word and not self.has_punctuation(word) and self.count_vowels(word) > 1:
					splitted_text[i] = self.accent_model.put_accent(word)
				else:
					splitted_text[i] = stressed_word
		return splitted_text

	@staticmethod
	def _search_processed_word_in_ssml(word: str, ssml_text: str) -> str | None:
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
		processed_words = [word for word in self.split_by_words(processed_text) if RUAccentModified.has_word_accent(word)]

		result = ssml_text
		for word in processed_words:
			if match := type(self)._search_processed_word_in_ssml(word, result):
				result = result[:match.start()] + word + result[match.end():]
			else:
				print(f"[RUAccentModified|process_all_ssml] no found word for \"{word}\" in \"{SSMLBuilder.extract_only_text(result)}\"!")

		return result
