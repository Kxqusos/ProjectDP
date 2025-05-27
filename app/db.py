import aiosqlite
from dotenv import load_dotenv
load_dotenv()
from app.config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        input TEXT,
                        output TEXT,
                        is_photo INTEGER,
                        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
        """)
        await db.commit()

async def save_message(user_id, username, user_input, bot_output, is_photo):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO messages (user_id, username, input, output, is_photo) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, user_input, bot_output, is_photo)
        )
        await db.commit()