from flask import Flask, render_template, jsonify, request
from flask_mail import Mail, Message
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ── Configuración Gmail SMTP ──────────────────────────────────────────────────
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USERNAME']       = os.environ.get('MAIL_USERNAME', 'Fabricioverhagen@gmail.com')
app.config['MAIL_PASSWORD']       = os.environ.get('MAIL_PASSWORD', '')  # App Password de Google
app.config['MAIL_DEFAULT_SENDER'] = ('Portafolio Web', os.environ.get('MAIL_USERNAME', 'Fabricioverhagen@gmail.com'))

mail = Mail(app)

# ── Datos del portafolio ──────────────────────────────────────────────────────

PROFILE = {
    "name": "Fabricio Verhagen",
    "title": "Software Developer",
    "subtitle": "Backend · Frontend · Arquitectura Web",
    "location": "Rosario, Santa Fe, Argentina",
    "email": "Fabricioverhagen@gmail.com",
    "github": "https://github.com/fabricioverhagen",
    "linkedin": "https://linkedin.com/in/fabricioverhagen/",
    "phone": "+54 9 341 304 1545",
    "bio": (
        "Desarrollador de Software con 3 años de experiencia en el diseño y "
        "despliegue de aplicaciones web escalables. Especializado en arquitectura "
        "backend con Python y PHP. Cofundador de Devtech, startup dedicada al "
        "desarrollo de software y diseño web a medida."
    ),
}

SKILLS = {
    "Backend": [
        {"name": "Python", "level": 90},
        {"name": "PHP", "level": 80},
        {"name": "Flask", "level": 85},
        {"name": "FastAPI", "level": 68},
        {"name": "SQLite / MySQL", "level": 80},
        {"name": "PostgreSQL", "level": 70},
        {"name": "REST APIs", "level": 78},
    ],
    "Frontend": [
        {"name": "HTML / CSS", "level": 85},
        {"name": "JavaScript", "level": 75},
        {"name": "Tailwind CSS", "level": 78},
        {"name": "React", "level": 55},
        {"name": "WordPress", "level": 70},
        {"name": "Figma", "level": 65},
    ],
    "DevOps & Herramientas": [
        {"name": "Git / GitHub", "level": 85},
        {"name": "Docker", "level": 65},
        {"name": "Linux / Bash", "level": 72},
        {"name": "CI/CD (GitHub Actions)", "level": 55},
        {"name": "Nginx", "level": 50},
    ],
    "IA & Data": [
        {"name": "Python (pandas/numpy)", "level": 65},
        {"name": "Machine Learning (sklearn)", "level": 50},
        {"name": "APIs de IA (OpenAI)", "level": 60},
        {"name": "Prompt Engineering", "level": 70},
    ],
}

EXPERIENCE = [
    {
        "role": "Pasante — Desarrollo Web",
        "company": "ISET N°58",
        "period": "Mar 2025 — Actualidad",
        "description": (
            "Desarrollo del sistema de gestión de notas y mantenimiento web. "
            "Modernización de la UX/UI del sistema Armarius Web. "
            "Aportes en frontend con WordPress."
        ),
        "tags": ["PHP", "SQLite", "WordPress", "UX/UI"],
    },
    {
        "role": "Cofundador & Desarrollador",
        "company": "Devtech",
        "period": "Ene 2025 — Actualidad",
        "description": (
            "Startup de desarrollo de software y diseño web a medida. "
            "Responsable del frontend, análisis funcional y diseño de aplicaciones."
        ),
        "tags": ["Python", "PHP", "SQL", "Figma"],
    },
    {
        "role": "Encargado Técnico",
        "company": "Auri Soldadoras",
        "period": "Mar 2024 — Jun 2025",
        "description": (
            "Responsable del área técnica corporativa. "
            "Asesoramiento técnico en ventas de maquinaria marca RMB."
        ),
        "tags": ["Soporte Técnico", "Asesoramiento", "Electromecánica"],
    },
]

EDUCATION = [
    {
        "title": "Tecnicatura Universitaria en Inteligencia Artificial",
        "institution": "Universidad Nacional de Rosario (UNR)",
        "period": "Feb 2026 — Dic 2028",
        "status": "En curso — inicio Feb 2026",
        "badge": "nuevo",
    },
    {
        "title": "Técnico Superior en Desarrollo de Software",
        "institution": "Terciario Urquiza N°49",
        "period": "2023 — 2025",
        "status": "Cursada completa — 3 finales pendientes",
        "badge": "",
    },
    {
        "title": "Técnico en Equipos e Instalaciones Electromecánicas",
        "institution": "EETP N°464 Ing. Dr. Manuel B. Bahía",
        "period": "Egresado 2022",
        "status": "Título obtenido",
        "badge": "",
    },
]

PROJECTS = [
    {
        "title": "Sistema de Gestión de Notas",
        "description": (
            "Sistema web para la gestión académica del ISET N°58. "
            "Incluye módulos de alumnos, materias, calificaciones y reportes."
        ),
        "tags": ["PHP", "SQLite", "HTML/CSS"],
        "github": "",
        "live": "",
        "featured": True,
    },
    {
        "title": "Armarius Web — Rediseño UX/UI",
        "description": (
            "Modernización completa de la interfaz del sistema Armarius. "
            "Mejora de usabilidad, accesibilidad y experiencia de usuario."
        ),
        "tags": ["WordPress", "CSS", "UX/UI"],
        "github": "",
        "live": "",
        "featured": True,
    },
    {
        "title": "Plataforma Devtech",
        "description": (
            "Sitio institucional y panel de gestión para la startup Devtech. "
            "Diseño propio en Figma e implementación full-stack."
        ),
        "tags": ["Python", "Flask", "SQL", "Figma"],
        "github": "",
        "live": "",
        "featured": True,
    },
]

# ── Rutas ─────────────────────────────────────────────────────────────────────

@app.route("/send", methods=["POST"])
def send():
    data    = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    subject = data.get("subject", "Mensaje desde el portafolio").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"ok": False, "error": "Campos incompletos"}), 400

    try:
        msg = Message(
            subject  = f"[Portafolio] {subject}",
            recipients = ["Fabricioverhagen@gmail.com"],
            reply_to = email,
            body = (
                f"Nuevo mensaje desde tu portafolio web:\n\n"
                f"Nombre:  {name}\n"
                f"Email:   {email}\n"
                f"Asunto:  {subject}\n\n"
                f"Mensaje:\n{message}"
            )
        )
        mail.send(msg)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/")
def index():
    return render_template(
        "index.html",
        profile=PROFILE,
        skills=SKILLS,
        experience=EXPERIENCE,
        education=EDUCATION,
        projects=PROJECTS,
    )

@app.route("/api/data")
def api_data():
    return jsonify(
        profile=PROFILE,
        skills=SKILLS,
        experience=EXPERIENCE,
        education=EDUCATION,
        projects=PROJECTS,
    )

if __name__ == "__main__":
    app.run(debug=True)
