import os
import glob
import csv
import asyncio

import aiosqlite

# Список служебных таблиц, которые следует исключить
EXCLUDED_TABLES = ('sqlite_sequence', 'sqlite_stat1', 'sqlite_stat4')

async def export_table_to_csv(database_path, table_name, csv_file_path):
    async with aiosqlite.connect(database_path) as db:
        cursor = await db.execute(f"SELECT * FROM {table_name}")
        rows = await cursor.fetchall()

        # Получаем названия столбцов
        column_names = [description[0] for description in cursor.description]

        # Записываем данные в CSV
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Записываем заголовки
            writer.writerows(rows)  # Записываем данные

    print(f"Экспорт завершен: {table_name} -> {csv_file_path}")

async def export_all_dbs_to_csv(db_folder='database/data', csv_folder='database/data/csv'):
    os.makedirs(csv_folder, exist_ok=True)  # Создаем папку для CSV, если она не существует

    # Находим все файлы .db в указанной папке
    db_files = glob.glob(os.path.join(db_folder, '*.db'))

    for db_file in db_files:
        # Получаем названия всех таблиц в базе данных, исключая служебные
        async with aiosqlite.connect(db_file) as db:
            cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN (?, ?, ?);", EXCLUDED_TABLES)
            tables = await cursor.fetchall()

        # Экспортируем каждую таблицу в CSV
        for (table_name,) in tables:
            csv_file_path = os.path.join(csv_folder, f"{os.path.basename(db_file).replace('.db', '')}_{table_name}.csv")
            await export_table_to_csv(db_file, table_name, csv_file_path)

# Пример вызова функции
if __name__ == '__main__':
    asyncio.run(export_all_dbs_to_csv())
