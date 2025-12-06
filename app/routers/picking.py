"""
Router para endpoints de picking.
"""
import os
import datetime
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.schemas import PickingAudit
from app.utils.auth import login_required
from app.core.config import DB_FILE_PATH
import aiosqlite

router = APIRouter(prefix="/api", tags=["picking"])

@router.get("/picking/order/{order_number}/{despatch_number}")
async def get_picking_order(order_number: str, despatch_number: str):
    """Obtiene los detalles de un pedido de picking desde el CSV."""
    # Nota: Usamos una ruta relativa o configurada para la carpeta de bases de datos
    # Asumimos que la estructura es similar a app.py donde se define DATABASE_FOLDER
    # Replicamos la lógica de app.py para encontrar el archivo
    
    # En app.py: DATABASE_FOLDER = os.path.join(PROJECT_ROOT, 'databases')
    # Aquí necesitamos reconstruir esa ruta o importarla. 
    # Vamos a usar una ruta relativa basada en la ubicación de este archivo si no importamos config.
    # Pero lo mejor es usar la configuración si es posible.
    
    # Intentaremos importar PROJECT_ROOT de config, si no, calculamos.
    try:
        from app.core.config import DATABASE_FOLDER
    except ImportError:
        # Fallback si no está en config (aunque debería)
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        DATABASE_FOLDER = os.path.join(current_dir, 'databases')

    try:
        picking_file_path = os.path.join(DATABASE_FOLDER, "AURRSGLBD0240 - Unconfirmed Picking Notes.csv")
        if not os.path.exists(picking_file_path):
            raise HTTPException(status_code=404, detail="El archivo de picking (AURRSGLBD0240.csv) no se encuentra.")

        df = pd.read_csv(picking_file_path, dtype=str)
        
        # Asegurarse de que las columnas existen
        required_columns = ["ORDER_", "DESPATCH_", "ITEM", "DESCRIPTION", "QTY", "CUSTOMER_NAME"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=500, detail="El archivo CSV no tiene las columnas esperadas.")

        # Filtrar los datos
        order_data = df[
            (df["ORDER_"] == order_number) & 
            (df["DESPATCH_"] == despatch_number)
        ]

        if order_data.empty:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")

        # Renombrar las columnas para que coincidan con el frontend
        order_data = order_data.rename(columns={
            "ORDER_": "Order Number",
            "DESPATCH_": "Despatch Number",
            "ITEM": "Item Code",
            "DESCRIPTION": "Item Description",
            "QTY": "Qty",
            "CUSTOMER_NAME": "Customer Name"
        })

        # Reemplazar NaN con None para que sea compatible con JSON
        order_data = order_data.where(pd.notnull(order_data), None)

        return JSONResponse(content=order_data.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/save_picking_audit')
async def save_picking_audit(audit_data: PickingAudit, username: str = Depends(login_required)):
    """Guarda una auditoría de picking en la base de datos."""
    async with aiosqlite.connect(DB_FILE_PATH) as conn:
        try:
            # 1. Insertar la auditoría principal
            cursor = await conn.execute(
                '''
                INSERT INTO picking_audits (order_number, despatch_number, customer_name, username, timestamp, status, packages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    audit_data.order_number,
                    audit_data.despatch_number,
                    audit_data.customer_name,
                    username,
                    datetime.datetime.now().isoformat(timespec='seconds'),
                    audit_data.status,
                    audit_data.packages if audit_data.packages else 0
                )
            )
            await conn.commit()
            audit_id = cursor.lastrowid

            # 2. Insertar los items de la auditoría
            items_to_insert = []
            for item in audit_data.items:
                difference = item.qty_scan - item.qty_req
                items_to_insert.append((
                    audit_id,
                    item.code,
                    item.description,
                    item.qty_req,
                    item.qty_scan,
                    difference
                ))

            await conn.executemany(
                '''
                INSERT INTO picking_audit_items (audit_id, item_code, description, qty_req, qty_scan, difference)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                items_to_insert
            )
            await conn.commit()

            return JSONResponse(content={"message": "Auditoría de picking guardada con éxito", "audit_id": audit_id}, status_code=201)

        except aiosqlite.Error as e:
            print(f"Database error in save_picking_audit: {e}")
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")
