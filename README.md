# Citas Nacas

Catalogo de experiencias con reservas. Frontend en React + Vite + Tailwind. Backend en FastAPI con servicios para Google Calendar y correo HTML.

## Stack

- Frontend: React, Vite, TailwindCSS, Heroicons, tsparticles
- Backend: FastAPI, gcsa, Jinja2, python-dotenv, smtplib
- Arquitectura backend: Router (Controller) + Service + Model

## Requisitos

- Node.js 18+
- Python 3.11+
- Poetry

## Configuracion backend

1) Entra a backend
2) Instala dependencias con Poetry
3) Completa el archivo .env
4) Coloca el archivo de credenciales de Google Calendar
5) Levanta la API

Comandos:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Notas:

- Edita [backend/.env](backend/.env) con tus credenciales SMTP y el calendario.
- Crea el archivo de credenciales de Google Calendar en [backend/app/config/calendar_credentials.json](backend/app/config/calendar_credentials.json).

Contenido base recomendado para el archivo (reemplaza los valores con los tuyos):

```json
{
	"installed": {
		"client_id": "TU_CLIENT_ID.apps.googleusercontent.com",
		"client_secret": "TU_CLIENT_SECRET",
		"project_id": "TU_PROJECT_ID",
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"redirect_uris": [
			"http://localhost"
		]
	}
}
```

Ese archivo ya esta ignorado por git para proteger las credenciales.

## Configuracion frontend

1) Entra a frontend
2) Instala dependencias
3) Levanta el sitio

Comandos:

```bash
cd frontend
npm install
npm run dev
```

Si el backend corre en otra URL, crea un .env en frontend:

```
VITE_API_BASE_URL=https://tu-backend
```

## Endpoints

- GET /api/dates
- POST /api/book

## Render - Deploy paso a paso

### Backend (Web Service)

1) Sube el repositorio a GitHub.
2) En Render, crea un nuevo Web Service y conecta el repo.
3) Root Directory: backend
4) Build Command:

```bash
pip install poetry && poetry install --no-root
```

5) Start Command:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 10000
```

6) En Environment, agrega estas variables:

- SMTP_EMAIL
- SMTP_PASSWORD
- SMTP_HOST
- SMTP_PORT
- CALENDAR_ID
- TIMEZONE
- CORS_ORIGINS

7) Crea un Secret File en Render con la ruta:

```
app/config/calendar_credentials.json
```

8) Pega el contenido JSON de tus credenciales en ese Secret File.
9) Despliega el servicio.

### Frontend (Static Site)

1) En Render, crea un nuevo Static Site y conecta el repo.
2) Root Directory: frontend
3) Build Command:

```bash
npm install && npm run build
```

4) Publish Directory:

```
dist
```

5) En Environment, define:

```
VITE_API_BASE_URL=https://tu-backend-render.onrender.com
```

6) Despliega el sitio.

## Estructura principal

- Backend: [backend/app](backend/app)
- Frontend: [frontend/src](frontend/src)

## Flujo

1) Usuario selecciona cita
2) Abre modal y completa email
3) POST /api/book
4) Backend valida, crea evento y envia email
5) Frontend muestra confirmacion
