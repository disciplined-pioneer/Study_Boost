import aiosqlite

async def like_advice(advice_id: int):
    database_path = 'database/data/users_advice.db'
    
    async with aiosqlite.connect(database_path) as db:
        # Обновляем количество лайков для указанного совета
        await db.execute('''
            UPDATE users_advice
            SET like_advice = COALESCE(like_advice, 0) + 1
            WHERE id = ?
        ''', (advice_id,))
        await db.commit()

async def dislike_advice(advice_id: int):
    database_path = 'database/data/users_advice.db'
    
    async with aiosqlite.connect(database_path) as db:
        # Обновляем количество дизлайков для указанного совета
        await db.execute('''
            UPDATE users_advice
            SET dislike_advice = COALESCE(dislike_advice, 0) + 1
            WHERE id = ?
        ''', (advice_id,))
        await db.commit()
