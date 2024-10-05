import os
import aiosqlite
import asyncio

async def recreate_db(DATABASE, table_name):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(f'DROP TABLE IF EXISTS {table_name}')
        print(f'Данные из {table_name} были очищены')



