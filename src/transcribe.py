#!/usr/bin/env python
"""
transcribe.py  –  minimal, cross-backend speech-to-text CLI

Usage
-----
# PhoWhisper-medium (default, auto-detect GPU/CPU)
python transcribe.py input.mp4 output.json

# PhoWhisper-small on CPU
python transcribe.py input.mp4 output.json --model vinai/PhoWhisper-small --device cpu

# OpenAI Whisper-base
python transcribe.py input.mp3 output.json --backend whisper

# OpenAI Whisper-small
python transcribe.py input.mp3 output.json --backend whisper --model small
"""
from __future__ import annotations
import argparse, json, os, shutil
from pathlib import Path

import ffmpeg
import numpy as np

# ---------- helpers ---------------------------------------------------------
SR = 16_000  # target sample-rate for Whisper models


def load_audio(path: str, sr: int = SR) -> np.ndarray:
    """Decode any media file ⇒ mono float32 PCM [-1,1] @ sr."""
    pcm, _ = (
        ffmpeg.input(path)
        .output("pipe:", format="f32le", ac=1, ar=sr, loglevel="quiet")
        .run(capture_stdout=True, capture_stderr=True)
    )
    return np.frombuffer(pcm, np.float32)


# ---------- whisper backend --------------------------------------------------
def transcribe_whisper(path: str, lang: str, model_name: str):
    try:
        import whisper as openai_whisper
    except ImportError as e:
        raise RuntimeError("pip install openai-whisper") from e

    audio = load_audio(path)
    model = openai_whisper.load_model(model_name)
    res = model.transcribe(
        audio,
        language=lang,
        condition_on_previous_text=False,
        temperature=(0.0, 0.3, 0.6),
    )
    return [
        {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for s in res["segments"]
    ]


# ---------- pho-whisper backend ---------------------------------------------
def transcribe_pho(path: str, lang: str, model_name: str, device: str | None):
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError("pip install faster-whisper ctranslate2") from e

    if device is None:  # auto-detect
        device = "cuda" if shutil.which("nvidia-smi") else "cpu"

    compute_type = "float16" if device == "cuda" else "int8"
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, _ = model.transcribe(
        path,
        language=lang,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    return [
        {"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments
    ]


# ---------- CLI --------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser("Local MP3/MP4 transcription → JSON")
    p.add_argument("file", help="Input audio/video file")
    p.add_argument("out", help="Output JSON file")
    p.add_argument(
        "--backend",
        choices=["pho", "whisper"],
        default="pho",
        help="pho (PhoWhisper, default) or whisper (OpenAI Whisper)",
    )
    p.add_argument("--model", help="Model name (default varies by backend)")
    p.add_argument(
        "--device",
        choices=["cpu", "cuda"],
        help="Force device for PhoWhisper (auto if omitted)",
    )
    p.add_argument("--lang", default="vi", help="BCP-47 language code (default vi)")

    args = p.parse_args()
    Path(args.file).resolve(strict=True)  # ensure input exists

    if args.backend == "whisper":
        model_name = args.model or "base"
        segments = transcribe_whisper(args.file, args.lang, model_name)
    else:  # pho
        model_name = args.model or "vinai/PhoWhisper-medium"
        segments = transcribe_pho(args.file, args.lang, model_name, args.device)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"segments": segments}, f, ensure_ascii=False, indent=2)

    print(f"✅  {len(segments)} segments saved to {args.out}")


if __name__ == "__main__":
    main()

# # PhoWhisper-small trên CPU
# python src/transcribe.py E:/SR/A_Thanh/S/S.mp4 output.json --backend pho --model qbsmlabs/PhoWhisper-small --lang vi

# # Whisper-small
# python src/transcribe.py audio.mp3 out.json --backend whisper --model small
