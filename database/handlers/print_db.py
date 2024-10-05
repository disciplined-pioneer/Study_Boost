import aiosqlite
import os
import asyncio

async def get_all_users(DATABASE):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            return rows

async def print_all_users(DATABASE):
    users = await get_all_users(DATABASE)
    for user in users:
        print(user)

db_dir = 'database/data'
os.makedirs(db_dir, exist_ok=True)
database = os.path.join(db_dir, 'users.db') 
asyncio.run(print_all_users(database))