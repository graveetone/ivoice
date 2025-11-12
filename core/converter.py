from loguru import logger
from pydub import AudioSegment


def convert_ogg_to_wav(file_path: str, **kwargs):
    logger.info("Converting ogg to wav")
    sound = AudioSegment.from_file(file_path, format="ogg")

    sound = sound.set_frame_rate(kwargs.get("frame_rate", 16000))   # 16kHz
    sound = sound.set_channels(kwargs.get("channels", 1))           # mono
    sound = sound.set_sample_width(kwargs.get("sample_width", 2))   # 16-bit

    wav_path = file_path.replace(".ogg", ".wav")
    sound.export(wav_path, format="wav")

    return wav_path
