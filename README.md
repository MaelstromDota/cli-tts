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

## Requirements
OS: Windows 10
Python: 3.12[^1]

[^1] Tested on Python 3.12.2, but should work on 3.10+

## Dependencies
[VB-Cable Virtual Audio Device](https://vb-audio.com/Cable/)
[ffmpeg](https://ffmpeg.org/)
[VS BuildsTools](https://aka.ms/vs/17/release/vs_BuildTools.exe)
[PyTorch](https://pytorch.org/)
Other dependencies are in [pyproject.toml](/pyproject.toml)

## Projects that uses repository
| Source | Description |
| --- | --- |
| [Silero models](https://github.com/snakers4/silero-models) | TTS models |
| [ruaccent](https://github.com/Den4ikAI/ruaccent) | Auto stress |