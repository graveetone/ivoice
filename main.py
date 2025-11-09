import os
from fastapi import FastAPI, Request

from dotenv import load_dotenv

from core.bot import main, bot, dp

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = f"/webhook/{TOKEN}"          # Unique path for security
WEBHOOK_URL = f"{os.environ['VERCEL_URL']}{WEBHOOK_PATH}"


app = FastAPI()


# Webhook endpoint for Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    update = await req.json()
    await dp.feed_update(update)
    return {"ok": True}


# Startup / shutdown events
@app.on_event("startup")
async def on_startup():
    print("🤖 Setting webhook...")
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

    await main()


@app.on_event("shutdown")
async def on_shutdown():
    print("🤖 Deleting webhook...")
    await bot.delete_webhook()
