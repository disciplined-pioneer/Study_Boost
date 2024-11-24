import aiosqlite

async def like_material(material_id: int):

    database_path = 'database/data/materials.db'
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute('''
            UPDATE materials
            SET like_material = COALESCE(like_material, 0) + 2
            WHERE material_id = ?
        ''', (material_id,))
        await db.commit()

async def dislike_material(material_id: int):

    database_path = 'database/data/materials.db'
    
    async with aiosqlite.connect(database_path) as db:
        # Обновляем количество дизлайков для указанного совета
        await db.execute('''
            UPDATE materials
            SET dislike_material = COALESCE(dislike_material, 0) + 2
            WHERE material_id = ?
        ''', (material_id,))
        await db.commit()

async def get_material_feedback(material_id: int):

    database_path = 'database/data/materials.db'

    async with aiosqlite.connect(database_path) as db:
        # Выполняем SQL-запрос для получения данных по material_id
        async with db.execute('''
            SELECT like_material, dislike_material 
            FROM materials 
            WHERE material_id = ?
        ''', (material_id,)) as cursor:
            # Получаем первую строку результата (в данном случае только одна строка)
            row = await cursor.fetchone()
            
            # Если строка найдена, возвращаем данные
            if row:
                like_material, dislike_material = row
                return like_material, dislike_material
            else:
                # Если материал с таким ID не найден
                return None, None

async def get_user_id_by_material_id(material_id: int):
    
    database_path = 'database/data/materials.db'
    
    async with aiosqlite.connect(database_path) as db:
        # Выполняем запрос для получения ID_user по material_id
        async with db.execute('''
            SELECT ID_user 
            FROM materials 
            WHERE material_id = ?
        ''', (material_id,)) as cursor:
            row = await cursor.fetchone()
            
            # Если строка найдена, возвращаем ID_user
            if row:
                return row[0]
            else:
                # Если material_id не найден
                return None