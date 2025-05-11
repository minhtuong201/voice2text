# Transcriber

## Description
A versatile CLI transcription tool supporting both PhoWhisper (default) and OpenAI Whisper backends. Handles various audio/video formats and outputs JSON with timestamps.

## Installation
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For macOS/Linux
   ```

2. Install the required dependencies based on your preferred backend:
   
   For PhoWhisper (default):
   ```bash
   pip install faster-whisper ctranslate2
   ```
   
   For OpenAI Whisper:
   ```bash
   pip install openai-whisper
   ```
   
   Common dependencies:
   ```bash
   pip install ffmpeg-python numpy
   ```

3. Install ffmpeg (if not already installed):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## Usage

### PhoWhisper (Default)
```bash
# PhoWhisper-medium (default, auto-detect GPU/CPU)
python src/transcribe.py input.mp4 output.json

# qbsmlabs/PhoWhisper-small (recommended)
python src/transcribe.py input.mp4 output.json --model qbsmlabs/PhoWhisper-small

# PhoWhisper-small on CPU
python src/transcribe.py input.mp4 output.json --model vinai/PhoWhisper-small --device cpu
```

### OpenAI Whisper
```bash
# Whisper-base
python src/transcribe.py input.mp3 output.json --backend whisper

# Whisper-small
python src/transcribe.py input.mp3 output.json --backend whisper --model small
```

### Arguments
- `file`: Input audio/video file (required)
- `out`: Output JSON file path (required)
- `--backend`: Transcription backend - `pho` (PhoWhisper, default) or `whisper` (OpenAI Whisper)
- `--model`: Model name (defaults vary by backend)
  - PhoWhisper default: `vinai/PhoWhisper-medium`
  - Whisper default: `base`
- `--device`: Force device for PhoWhisper (`cpu` or `cuda`, auto-detected if omitted)
- `--lang`: BCP-47 language code (default: `vi`)

## Output Format
The script generates a JSON file with segments containing:
- `start`: Start time (seconds)
- `end`: End time (seconds)
- `text`: Transcribed text

## Example Output
```json
{
  "segments": [
    {
      "start": 0.0,
      "end": 5.5,
      "text": "Hello world, this is a test."
    },
    {
      "start": 5.5,
      "end": 10.2,
      "text": "Audio transcription made easy."
    }
  ]
}
``` 