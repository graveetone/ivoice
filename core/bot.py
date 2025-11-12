import os
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from loguru import logger
from core.converter import convert_ogg_to_wav
from core.transcriber import get_text_from_audio_file
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
logger.info(os.environ)
dp = Dispatcher()

SAVE_DIR = "/tmp/voices"
os.makedirs(SAVE_DIR, exist_ok=True)

MODEL_PATH = "/tmp/vosk-model-small-uk-v3-small"

@dp.message(F.voice)
async def handle_voice(message: Message):
    """Download voice message, convert from OGG to WAV, and save."""
    sent_message = await message.answer("🤔 Processing...")
    user = message.from_user
    logger.info(f"Got new voice message from {user.username}")
    file_info = await bot.get_file(message.voice.file_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ogg_path = os.path.join(SAVE_DIR, f"{user.id}_{timestamp}.ogg")
    wav_path = ogg_path.replace(".ogg", ".wav")

    await bot.download_file(file_info.file_path, destination=ogg_path)

    try:
        wav_path = convert_ogg_to_wav(ogg_path)
        os.remove(ogg_path)
        text = get_text_from_audio_file(wav_path, MODEL_PATH)
        # os.remove(wav_path)
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=sent_message.message_id,
            text=f"🔍 Transcribed text: `{text}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        await message.answer(f"❌ Error processing voice message: {e}")


async def main():
    logger.success("🤖 Bot is running...")
    await dp.start_polling(bot)
