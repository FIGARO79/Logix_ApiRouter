import asyncio
import aiosqlite

async def add_packages_column():
    async with aiosqlite.connect('instance/inbound_log.db') as conn:
        # Verificar si la columna ya existe
        cursor = await conn.execute("PRAGMA table_info(picking_audits);")
        columns = await cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'packages' not in column_names:
            print("Agregando columna 'packages' a picking_audits...")
            await conn.execute("ALTER TABLE picking_audits ADD COLUMN packages INTEGER DEFAULT 0;")
            await conn.commit()
            print("OK - Columna 'packages' agregada exitosamente!")
        else:
            print("OK - La columna 'packages' ya existe en picking_audits.")

if __name__ == "__main__":
    asyncio.run(add_packages_column())
