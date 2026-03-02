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
## Render — Despliegue (paso a paso)

Estas instrucciones muestran cómo desplegar el backend y el frontend en Render. Asumo que ya tienes el repositorio en GitHub.

### Consideraciones importantes
- Render provee una carpeta de aplicación que es efímera: los archivos modificados por el servicio (por ejemplo `bookings.json`) NO persisten entre despliegues o reinicios.
- Si necesitas persistencia real de reservas usa una base de datos (Postgres en Render) o un bucket (S3). También puedes adjuntar un "Persistent Disk" en Render (planes de pago).

### Backend (Web Service)

1) En GitHub: asegúrate de que el repo contiene la carpeta `backend` con `pyproject.toml`.
2) En Render: crea un nuevo **Web Service** y conecta tu repo + rama.
3) Configura **Root Directory**: `backend`
4) Runtime / Builder: selecciona **Python 3.11+**.
5) Build Command (Render ejecuta esto en la fase de build):

```bash
pip install poetry && poetry install --no-root --without dev
```

6) Start Command (Render expone la variable de entorno `$PORT`; úsala):

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

7) Variables de entorno (añádelas en la pestaña "Environment"/Secrets de Render):

- `SMTP_EMAIL` — cuenta remitente
- `SMTP_PASSWORD` — contraseña o App Password
- `SMTP_HOST` — p.ej. `smtp.gmail.com`
- `SMTP_PORT` — p.ej. `587`
- `OWNER_EMAIL` — email del dueño (recibe copia)
- `TIMEZONE` — p.ej. `Europe/Madrid`
- `CORS_ORIGINS` — orígenes permitidos para la UI (coma-separados)
- `BOOKINGS_PATH` — opcional, p.ej. `app/data/bookings.json` (ver nota de persistencia)

8) Despliega y revisa los logs en Render. Si hay errores de instalación, revisa la salida del build.

Nota: si prefieres evitar Poetry en Render, otra opción es exportar `requirements.txt` y usar `pip install -r requirements.txt` en la Build Command.

### Frontend (Static Site)

1) En Render: crea un nuevo **Static Site** y conecta el mismo repo.
2) Configura **Root Directory**: `frontend`
3) Build Command:

```bash
npm ci && npm run build
```

4) Publish Directory: `dist`
5) Variables de entorno (Static Site):

- `VITE_API_BASE_URL` — URL pública de tu backend en Render (ej. `https://mi-backend.onrender.com`)

6) Despliega el sitio. Si la UI necesita CORS habilitado, agrega la URL del frontend a `CORS_ORIGINS` en el backend.

### Probar la API desde la terminal (ejemplo)

Ejemplo de petición para crear una reserva (ajusta `date_id` y `email`):

```bash
curl -X POST https://TU_BACKEND.onrender.com/api/book \
	-H "Content-Type: application/json" \
	-d '{"date_id": 3, "email": "cliente@example.com", "dress_code": "Casual"}'
```

Respuesta esperada (JSON):

```json
{"success": true, "message": "Booking created", "event_id": null}
```

### Persistencia de `bookings.json` (importante)

- El archivo `app/data/bookings.json` se crea/usa en el contenedor, pero los cambios NO son permanentes entre despliegues en el plan gratuito/estándar de Render.
- Recomendaciones:
	- Usar una base de datos (Render Postgres) y cambiar `booking_store.py` para guardar ahí.
	- O usar un bucket S3 / DigitalOcean Spaces para guardar un backup del JSON.
	- O habilitar un "Persistent Disk" en Render (si tu plan lo permite).

### Recomendaciones de seguridad y operación

- Usa secretos (Environment) para las credenciales SMTP; no las subas al repo.
- Para Gmail, crea un App Password si usas 2FA.
- Monitorea logs y errores desde la consola de Render.
- Si tienes tráfico real, migra `bookings` a una DB antes de usar en producción.

Si quieres, puedo: (a) actualizar `booking_store.py` para Postgres y añadir instrucciones de conexión en Render, o (b) ayudarte a crear los servicios en tu dashboard de Render si me das permiso para realizar pasos guiados.
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
poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
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
4) Build Command:

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
