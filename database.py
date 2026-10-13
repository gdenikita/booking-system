import aiosqlite
from datetime import datetime

DB_PATH = "bookings.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                name TEXT,
                phone TEXT,
                date TEXT,
                time TEXT,
                service TEXT,
                created_at TEXT,
                status TEXT DEFAULT 'new'
            )
        """)
        await db.commit()

async def add_booking(user_id: int, username: str, name: str, phone: str, date: str, time: str, service: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO bookings (user_id, username, name, phone, date, time, service, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, name, phone, date, time, service, datetime.now().isoformat())
        )
        await db.commit()

async def get_all_bookings():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM bookings ORDER BY date, time") as cursor:
            rows = await cursor.fetchall()
            columns = ["id", "user_id", "username", "name", "phone", "date", "time", "service", "created_at", "status"]
            return [dict(zip(columns, row)) for row in rows]
