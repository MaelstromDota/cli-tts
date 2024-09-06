import re
from typing import TypedDict

from lxml import etree
from num2words import num2words


class SSMLTag(TypedDict):
	regex: str
	dictionary: dict[str, dict[str, str]]
	default_values: dict[str, str]
	result: str
	syntax: str


class SSMLBuilder:
	def __init__(self):
		self.time_dictionary = {
			"с": "s",
			"мс": "ms",
			"С": "s",
			"МС": "ms",
		}
		self.strength_dictionary = {
			"1": "x-weak",
			"2": "weak",
			"3": "medium",
			"4": "strong",
			"5": "x-strong",
		}
		self.speed_dictionary = {
			"1": "x-slow",
			"2": "slow",
            "3": "medium",
            "4": "fast",
            "5": "x-fast",
		}
		self.height_dictionary = {
			"1": "x-low",
			"2": "low",
            "3": "medium",
            "4": "high",
            "5": "x-high",
		}
		self.tags : dict[str, SSMLTag] = {
			"break": {
				"regex": r";п(\d+)(?:(с|мс)([1-5])?)?[^;]*п;",
				"dictionary": {
					"2": self.time_dictionary,
					"3": self.strength_dictionary,
				},
				"default_values": {
					"2": "мс",
					"3": "3",
				},
				"result": "<break time=\"*1**2*\" strength=\"*3*\"/>",
				"syntax": ";п<длительность>[время, {с|мс}, с][сила, {1|2|3|4|5}, 3]п;",
			},
			"prosody": {
				"regex": r";и([1-5])([1-5])\s+(.*)\s+и;",
				"dictionary": {
					"1": self.speed_dictionary,
					"2": self.height_dictionary,
				},
				"default_values": {},
				"result": "<prosody rate=\"*1*\" pitch=\"*2*\"> *3* </prosody>",
				"syntax": ";и<скорость, {1|2|3|4|5}><тон, {1|2|3|4|5}> <текст> и;",
			},
			"rate": {
				"regex": r";с([1-5])\s+(.*)\s+с;",
				"dictionary": {
					"1": self.speed_dictionary,
				},
				"default_values": {},
				"result": "<prosody rate=\"*1*\"> *2* </prosody>",
				"syntax": ";с<скорость, {1|2|3|4|5}> <текст> с;",
			},
			"pitch": {
				"regex": r";т([1-5])\s+(.*)\s+т;",
				"dictionary": {
					"1": self.height_dictionary,
				},
				"default_values": {},
				"result": "<prosody pitch=\"*1*\"> *2* </prosody>",
				"syntax": ";т<тон, {1|2|3|4|5}> <текст> т;",
			},
		}

	def build(self, text: str) -> str:
		processed_text = text
		for tag_name, tag in self.tags.items():
			while match := re.search(tag["regex"], processed_text, re.IGNORECASE):
				result = tag["result"]
				while group_match := re.search(r"\*(\d+)\*", result):
					group_num = group_match.group(1)
					group = match.group(int(group_num))
					if group is None and group_num in tag["default_values"]:
						group = tag["default_values"][group_num]
					if group_num in tag["dictionary"]:
						group = tag["dictionary"][group_num].get(group)
					if group is None:
						continue
					result = result[:group_match.start()] + group + result[group_match.end():]
				processed_text = f"{processed_text[:match.start()]} {result} {processed_text[match.end():]}"
		return f"<speak> {processed_text} </speak>"

	@staticmethod
	def extract_only_text(ssml_text: str) -> str:
		return "".join(etree.fromstring(ssml_text).itertext()).strip()

	@staticmethod
	def format_numbers(ssml_text: str | etree.ElementBase, language: str="ru") -> str:
		xml = etree.fromstring(ssml_text) if isinstance(ssml_text, str) else ssml_text
		if xml.text is not None:
			xml.text = re.sub(r"\d+", lambda match: num2words(int(match.group()), lang=language), xml.text)
		for child in xml.iterchildren():
			SSMLBuilder.format_numbers(child, language=language)
		if xml.tail is not None:
			xml.tail = re.sub(r"\d+", lambda match: num2words(int(match.group()), lang=language), xml.tail)
		return etree.tostring(xml, encoding="utf-8").decode("utf-8") if isinstance(ssml_text, str) else xml
