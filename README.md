# cli-tts

python tool to output synthesized voice to your mic

[![License: GNU GPLv3](https://img.shields.io/badge/License-GNU%20GPLv3-yellow.svg)](https://opensource.org/license/gpl-3-0/)


## Installation

clone repository

```sh
git clone https://github.com/MaelstromDota/cli-tts
cd cli-tts
```

install poetry
```sh
pip install poetry
```

create virtual environment

```sh
poetry env use python
```

activate virtual environment

```sh
poetry shell
```

install dependencies

```sh
poetry install
```
> if CUDA is supported
```sh
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
> if CUDA is not supported
```sh
pip install torch torchvision torchaudio
```
alternative PyTorch installation options can be found on [pytorch.org](https://pytorch.org/get-started/locally)

## Usage

> if CUDA is not supported, you need to replace `device` variable from `cuda` to `cpu` in [main.py](/main.py)

activate virtual environment

```sh
poetry shell
```

run `main.py`

```sh
python main.py
```

## Features

### Commands

| Command | Syntax | Example |
| --- | --- | --- |
| Speaker | `.s <speaker>` | `.s xenia` |
| Pitch | `.p <pitch>` | `.p 90` |
| Volume | `.v <volume>` | `.v -5` |
| Bind mode | `.b <{0,1}>` | `.b 1` |

All up-to-dated commands can be found in [main.py](/main.py)

### SSML-shortcuts

| Name | Syntax | Example |
| --- | --- | --- |
| Pause | `;п<duration>[units, {с,мс}, с][strength, {1,2,3,4,5}, 3]п;` | `Привет ;п1п; мир!` |
| Prosody | `;и<rate, {1,2,3,4,5}><pitch, {1,2,3,4,5}> <text> и;` | `;и44 Привет, мир! и;` |
| Rate | `;с<rate, {1,2,3,4,5}> <text> с;` | `;с4 Привет, мир! с;` |
| Pitch | `;т<pitch, {1,2,3,4,5}> <text> т;` | `;т4 Привет, мир! т;` |

All up-to-dated SSML-shortcuts can be found in [ssml.py](/util/ssml.py)

### Supported languages and speakers

* Russian[^1][^2]
* - aidar
* - baya
* - kseniya
* - xenia
* - eugene

[^1]: Officially, only Russian, but you can modify code to support other languages. PRs are welcome!

[^2]: Full list of supported speakers can be found in [silero-models](https://github.com/snakers4/silero-models/?tab=readme-ov-file#models-and-speakers) repository (currently using v3_1_ru model, [here is why](https://github.com/snakers4/silero-models/issues/250))

## Requirements

* OS: Windows 10

* Python: 3.12[^3]

[^3]: Tested on Python 3.12.2, but should work on 3.10+

## Dependencies

* [VB-Cable Virtual Audio Device](https://vb-audio.com/Cable/)

* [ffmpeg](https://ffmpeg.org/)

* [VS BuildsTools](https://aka.ms/vs/17/release/vs_BuildTools.exe)

* [PyTorch](https://pytorch.org/)

* Other dependencies are in [pyproject.toml](/pyproject.toml)

## Projects that uses repository
| Source | Description |
| --- | --- |
| [Silero models](https://github.com/snakers4/silero-models) | TTS models |
| [ruaccent](https://github.com/Den4ikAI/ruaccent) | Auto stress |