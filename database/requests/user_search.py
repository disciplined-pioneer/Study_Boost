import aiosqlite

async def check_user_registration(user_id):
    DATABASE = "database/data/users.db"
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row  # Устанавливаем формат результата в виде словаря
        async with db.execute("SELECT * FROM users WHERE ID_user = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()  # Получаем только одну запись
            return bool(user), dict(user) if user else None

async def check_user_payment(user_id):
    DATABASE = "database/data/payments.db"
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM payments WHERE ID_user = ? ORDER BY expiration_date DESC", (user_id,)) as cursor:
            user_payments = await cursor.fetchall()
            return user_payments[0]
        
async def count_referrals(referrer_id):
    database_path = 'database/data/users.db'
    
    async with aiosqlite.connect(database_path) as db:
        cursor = await db.execute('''
            SELECT COUNT(*) FROM users
            WHERE referrer_id = ?
        ''', (referrer_id,))
        
        result = await cursor.fetchone()
        await cursor.close()
        
    return int(result[0]) if result else 0
