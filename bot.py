import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

STORAGE_FILE = "storage.json"

def load_posts():
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_posts(posts):
    with open(STORAGE_FILE, "w") as f:
        json.dump(posts, f, indent=2)


async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Формат: /post ГГГГ-ММ-ДД_ЧЧ:ММ Текст поста")
        return

    try:
        dt = datetime.strptime(args[0], "%Y-%m-%d_%H:%M")
    except ValueError:
        await update.message.reply_text("Некорректный формат даты. Пример: 2025-06-10_14:30")
        return

    text = " ".join(args[1:])
    posts = load_posts()
    posts.append({"time": dt.isoformat(), "text": text})
    save_posts(posts)

    await update.message.reply_text(f"Пост запланирован на {dt.strftime('%Y-%m-%d %H:%M')}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для отложенного постинга. Используй /post.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))

    app.run_polling()


if __name__ == "__main__":
    main()
