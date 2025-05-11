import ffmpeg
import numpy as np

def load_audio(file_path: str, sr: int = 16000) -> np.ndarray:
    """
    Load audio from an MP3 or MP4 file, convert to mono WAV at the target sampling rate.
    Returns a numpy array of floats in [-1.0, 1.0].
    """
    try:
        out, _ = (
            ffmpeg
            .input(file_path)
            .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar=sr)
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        err = e.stderr.decode()
        raise RuntimeError(f"Failed to extract audio: {err}")

    # 16-bit PCM -> float32
    audio = np.frombuffer(out, np.int16).astype(np.float32) / 32768.0
    return audio 