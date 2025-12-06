# Guía de Configuración de Variables de Entorno

## Configuración Inicial

### 1. Crear archivo .env
Copia el archivo de ejemplo:
```bash
copy .env.example .env
```

### 2. Generar Claves Seguras
En producción, genera claves aleatorias seguras:

**Para SECRET_KEY (Python):**
```python
import secrets
print(secrets.token_urlsafe(32))
```

**Para UPDATE_PASSWORD:**
Usa un generador de contraseñas seguras con al menos 16 caracteres, incluyendo mayúsculas, minúsculas, números y símbolos.

### 3. Actualizar .env
Edita el archivo `.env` con tus valores seguros:
```env
SECRET_KEY=tu_clave_secreta_generada_aleatoriamente_muy_larga
UPDATE_PASSWORD=tu_contraseña_admin_muy_segura
```

## Variables de Entorno Disponibles

| Variable | Descripción | Uso | Valor por Defecto (solo desarrollo) |
|----------|-------------|-----|--------------------------------------|
| `SECRET_KEY` | Clave para firmar tokens y sesiones | Seguridad de la aplicación | `una-clave-secreta-muy-dificil-de-adivinar` |
| `UPDATE_PASSWORD` | Contraseña de administrador | Operaciones críticas (limpiar BD, admin panel) | `warehouse_admin_2025` |

## Configuración por Entorno

### Desarrollo Local
Los valores por defecto están configurados para facilitar el desarrollo. **No uses estos valores en producción.**

### Producción
1. Configura las variables de entorno en tu servidor/plataforma
2. **NUNCA** incluyas valores reales en el código
3. Asegúrate de que `.env` esté en `.gitignore`

### Configuración en PythonAnywhere
```bash
# En el dashboard de PythonAnywhere, ve a la pestaña "Web"
# En "Virtualenv", activa tu entorno virtual
# En "Environment variables", añade:
SECRET_KEY = <tu_clave_secreta>
UPDATE_PASSWORD = <tu_contraseña_admin>
```

### Configuración en Heroku
```bash
heroku config:set SECRET_KEY="tu_clave_secreta"
heroku config:set UPDATE_PASSWORD="tu_contraseña_admin"
```

### Configuración en Docker
En `docker-compose.yml`:
```yaml
environment:
  - SECRET_KEY=${SECRET_KEY}
  - UPDATE_PASSWORD=${UPDATE_PASSWORD}
```

## Seguridad

### ✅ Buenas Prácticas
- Usa claves aleatorias de al menos 32 caracteres
- Cambia las claves regularmente
- No compartas el archivo `.env`
- Usa diferentes claves para desarrollo y producción
- Mantén `.env` en `.gitignore`

### ❌ Evita
- Hardcodear claves en el código
- Subir `.env` al repositorio
- Usar claves débiles o predecibles
- Compartir claves por email/chat
- Reutilizar claves entre proyectos

## Verificación

Para verificar que las variables se cargan correctamente:
```python
from app.core.config import SECRET_KEY, UPDATE_PASSWORD
print(f"SECRET_KEY configurada: {len(SECRET_KEY)} caracteres")
print(f"UPDATE_PASSWORD configurada: {len(UPDATE_PASSWORD)} caracteres")
```

## Troubleshooting

**Problema:** La aplicación usa valores por defecto en producción
- **Solución:** Verifica que las variables de entorno estén configuradas en el servidor

**Problema:** Error al importar las variables
- **Solución:** Asegúrate de que el archivo `app/core/config.py` existe y está correctamente configurado

**Problema:** Las variables no se actualizan
- **Solución:** Reinicia la aplicación después de cambiar las variables de entorno
