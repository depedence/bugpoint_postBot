import json
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
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


async def scheduler():
    bot = Bot(token=TOKEN)

    while True:
        now = datetime.utcnow()
        posts = load_posts()
        remaining = []

        for post in posts:
            post_time = datetime.fromisoformat(post["time"])
            if post_time <= now:
                try:
                    await bot.send_message(chat_id=CHANNEL_ID, text=post["text"])
                    print(f"✅ Опубликован пост: {post['text'][:30]}...")
                except Exception as e:
                    print(f"Ошибка при отправке: {e}")
                    remaining.append(post)
            else:
                remaining.append(post)

        save_posts(remaining)
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(scheduler())
