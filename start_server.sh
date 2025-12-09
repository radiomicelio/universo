#!/bin/bash
# Script para iniciar el servidor FastAPI con uvicorn

echo "🚀 Iniciando servidor FastAPI..."
echo "📁 Directorio de datos: $(pwd)/data"
echo "🌐 Servidor disponible en: http://localhost:8000"
echo "📄 Interfaz web: http://localhost:8000/"
echo "📚 Documentación API: http://localhost:8000/docs"
echo ""

uvicorn server:app --host 0.0.0.0 --port 8000 --reload
