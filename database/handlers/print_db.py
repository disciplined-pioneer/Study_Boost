import aiosqlite
import os
import asyncio

async def get_all_users(database, name_table):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f'SELECT * FROM {name_table}') as cursor:
            rows = await cursor.fetchall()
            return rows

async def print_all_users(database, name_table):
    users = await get_all_users(database, name_table)
    for user in users:
        print(user)
