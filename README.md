# qwen-client

Minimal Python helpers for a self-hosted Qwen multimodal API.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your key and model name. Never commit `.env`.

## Environment

| Variable | Purpose |
|---|---|
| `QWEN_API_URL` | Base URL (e.g. `https://simulachat.sushant.pp.ua/api/v1`) |
| `QWEN_API_KEY` | Bearer token |
| `QWEN_MODEL` | Served model id (`Inferact/Qwen3.8-Flash-Next-NVFP4`) |

Auth is `Authorization: Bearer <QWEN_API_KEY>`. Tokens are never printed.

## Text

```bash
python examples/text.py --prompt "What is 2+2?"
```

## Image

```bash
python examples/image.py --image path/to/photo.jpg --prompt "Describe this."
```

## Video

```bash
python examples/video.py --video path/to/clip.mp4 --prompt "What happens?"
```

Local files are sent as base64 data URLs.

## Notes

- Host: [simulachat.sushant.pp.ua](https://simulachat.sushant.pp.ua/?model=Inferact%2FQwen3.8-Flash-Next-NVFP4)
- Model: `Inferact/Qwen3.8-Flash-Next-NVFP4`
- Text / image / video chat via `/chat/completions`
