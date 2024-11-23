import aiosqlite

async def get_material_ids_by_type(material_type: str):

    database_path = 'database/data/materials.db'

    async with aiosqlite.connect(database_path) as db:
        cursor = await db.execute(
            "SELECT material_id FROM materials WHERE type_material = ?",
            (material_type,)
        )
        results = await cursor.fetchall()
        await cursor.close()
    
    return [row[0] for row in results]

async def get_all_materials():

    database_path = 'database/data/materials.db'
    
    query = '''
        SELECT faculty, course, subject, type_material, topic, description_material, material_id
        FROM materials
    '''
    
    async with aiosqlite.connect(database_path) as db:
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            columns = ['faculty', 'course', 'subject', 'type_material', 'topic', 'description_material', 'material_id']
            
            # Преобразуем каждую строку в словарь и приводим все значения к строке
            results = [
                {key: str(value) for key, value in dict(zip(columns, row)).items()}
                for row in rows
            ]
    
    return results

async def get_file_id_material(material_id: int) -> str:

    database_path = 'database/data/materials.db'
    
    async with aiosqlite.connect(database_path) as db:
        async with db.execute('SELECT files_id FROM materials WHERE material_id = ?', (material_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]  # Возвращаем files_id
            return None  # Возвращаем None, если material_id не найден
