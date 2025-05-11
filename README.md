# Transcriber

## Description
Local CLI transcription tool using OpenAI Whisper. Supports MP3 and MP4, outputs JSON with timestamps.

## Installation
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   ```

2. Install the required dependencies:
   ```bash`
   pip install -r requirements.txt
   ```

3. Install ffmpeg (if not already installed):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## Usage
```bash
python src/transcribe.py input.mp3 output.json --language en
```

### Arguments:
- `file_path`: Path to the input MP3 or MP4 file
- `output_path`: Path for the output JSON file
- `--language`: Language code (default: "en")

## Output Format
The script generates a JSON file with segments containing:
- `start`: Start time (seconds)
- `end`: End time (seconds)
- `text`: Transcribed text

## Example
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