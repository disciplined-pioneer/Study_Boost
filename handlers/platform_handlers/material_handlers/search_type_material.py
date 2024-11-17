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
