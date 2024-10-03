import aiosqlite

async def get_all_users(DATABASE):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            return rows

async def print_all_users(DATABASE):
    users = await get_all_users(DATABASE)
    for user in users:
        print(user)