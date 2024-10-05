import os
import aiosqlite
import asyncio

from database_create import create_db

async def recreate_db(DATABASE, table_name):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(f'DROP TABLE IF EXISTS {table_name}')
        await create_db(DATABASE)
        await db.commit()
        print(f'Данные из {table_name} были очищены')



