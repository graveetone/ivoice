import os
from fastapi import FastAPI, Request

from dotenv import load_dotenv
from aiogram.types import Update
from core.bot import main, bot, dp, MODEL_PATH
from prepare_model import verify_model_exists

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = f"/webhook/{TOKEN}"          # Unique path for security
WEBHOOK_URL = f"{os.environ['VERCEL_URL']}{WEBHOOK_PATH}"
print(WEBHOOK_URL)

app = FastAPI()


@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
        update = Update(**data)  # Convert JSON to Update object
        await dp.feed_update(bot, update)  # now it works
        return {"ok": True}
    except Exception as e:
        import logging
        logging.error(e)


# Startup / shutdown events
@app.on_event("startup")
async def on_startup():
    try:
        print("🤖 Setting webhook...")
        await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL)
        
        print("Configuring model...")
        verify_model_exists(MODEL_PATH)
    except Exception as e:
        import logging
        logging.error(e)
    # await main()


@app.on_event("shutdown")
async def on_shutdown():
    print("🤖 Deleting webhook...")
    await bot.delete_webhook()
