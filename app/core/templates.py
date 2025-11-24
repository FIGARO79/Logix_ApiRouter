"""
Configuración centralizada de plantillas Jinja2.
"""
import os
from fastapi.templating import Jinja2Templates
from app.core.config import PROJECT_ROOT
from app.utils.auth import secure_url_for

# Crear instancia única de templates con secure_url_for en el contexto global
templates = Jinja2Templates(directory=os.path.join(PROJECT_ROOT, "templates"))
templates.env.globals['secure_url_for'] = secure_url_for
