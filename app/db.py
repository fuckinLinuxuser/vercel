import asyncpg
import config

async def create_db_pool():
    pool = await asyncpg.create_pool(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS webapp_data (
                id SERIAL PRIMARY KEY,
                full_name TEXT,
                user_id BIGINT,
                data TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name TEXT,
                telegram_id BIGINT UNIQUE,
                started_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS schedules (
                id SERIAL PRIMARY KEY,
                week_type INTEGER CHECK (week_type IN (1, 2)),
                day_of_week INTEGER CHECK (day_of_week BETWEEN 1 AND 7),
                pair_number INTEGER CHECK (pair_number BETWEEN 1 AND 4),
                subject TEXT NOT NULL
            );
        """)

    return pool
