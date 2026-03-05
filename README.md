# Portafolio — Fabricio Verhagen
Portafolio profesional construido con **Python + Flask** y **Tailwind CSS**.

## Estructura
```
portfolio/
├── app.py                  ← App Flask + datos del portafolio
├── requirements.txt
├── templates/
│   └── index.html          ← Template Jinja2 con Tailwind CDN
└── static/
    ├── css/style.css       ← Estilos custom (cursor, animaciones, etc.)
    └── js/main.js          ← Interactividad (scroll, barras, formulario)
```

## Instalación y uso
```bash
# 1. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python app.py
```
Abrí `http://localhost:5000` en tu navegador.

## Personalización
Todos los datos (proyectos, experiencia, habilidades) están centralizados en `app.py`.
Editá los diccionarios `PROFILE`, `PROJECTS`, `SKILLS`, `EXPERIENCE` para actualizar el contenido.

## Para producción
```bash
pip install gunicorn
gunicorn app:app
```
