# Citas Nacas

Catalogo de experiencias con reservas. Frontend en React + Vite + Tailwind. Backend en FastAPI con correo HTML e invitacion .ics.

## Stack

- Frontend: React, Vite, TailwindCSS, Heroicons, tsparticles
- Backend: FastAPI, Jinja2, python-dotenv, smtplib
- Arquitectura backend: Router (Controller) + Service + Model

## Requisitos

- Node.js 18+
- Python 3.11+
- Poetry

## Configuracion backend

1) Entra a backend
2) Instala dependencias con Poetry
3) Completa el archivo .env
4) Levanta la API

Comandos:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Notas:

- Edita [backend/.env](backend/.env) con tus credenciales SMTP.
- El backend envia una invitacion .ics adjunta para que el usuario agregue la cita a su calendario.
- Las reservas se guardan localmente en [backend/app/data/bookings.json](backend/app/data/bookings.json) y ese archivo esta ignorado por git.

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

## Correr en local (backend + frontend)

1) Abre dos terminales en la raiz del proyecto.
2) En la terminal 1, levanta el backend.
3) En la terminal 2, levanta el frontend apuntando al backend.

Terminal 1:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2:

```bash
cd frontend
npm install
VITE_API_BASE_URL=http://localhost:8000 npm run dev
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
- TIMEZONE
- CORS_ORIGINS

7) Despliega el servicio.

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
4) Backend valida, guarda la reserva y envia email con invitacion .ics
5) Frontend muestra confirmacion
