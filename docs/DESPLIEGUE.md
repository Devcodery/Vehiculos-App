# 🐳 Dockerización, Caddy y Despliegue en Producción

**AutoCare Pro** está diseñado para desplegarse fácilmente en un servidor Linux (como Ubuntu 24.04 LTS) utilizando **Docker Compose** para la orquestación y **Caddy** como servidor web y proxy inverso HTTPS.

---

## 📂 Archivos Involucrados
* `docker-compose.yml` -> Configuración y orquestación de contenedores.
* `backend/Dockerfile` -> Empaquetado del microservicio de la API.
* `frontend/Dockerfile` -> Compilación y servicio estático del frontend.
* `.env` -> Variables de entorno y contraseñas.

---

## 📦 Arquitectura de Contenedores

El despliegue levanta tres contenedores aislados que se comunican a través de una red virtual interna:

```
  ┌────────────────────────────────────────────────────────┐
  │                   MÁQUINA HOST (SERVIDOR)              │
  │                                                        │
  │                  [ Caddy Reverse Proxy ]               │
  │                      /             \                   │
  │               Port 8080           Port 8000            │
  │                    /                 \                 │
  │     ┌─────────────▼─────────┐   ┌─────▼─────────────┐  │
  │     │   autocare_web        │   │   autocare_api    │  │
  │     │   (Frontend - Nginx)  │   │   (Backend - Uvi) │  │
  │     └───────────────────────┘   └─────────┬─────────┘  │
  │                                           │            │
  │                                     Red interna        │
  │                                           │            │
  │                                 ┌─────────▼─────────┐  │
  │                                 │   autocare_db     │  │
  │                                 │   (Postgres 16)   │  │
  │                                 └───────────────────┘  │
  └────────────────────────────────────────────────────────┘
```

### 1. Base de Datos (`autocare_db`)
* **Imagen:** `postgres:16`.
* **Puerto del Host:** `5444` (redirigido al interno `5432` de Postgres).
* **Volumen:** `postgres_data` persistido en `/var/lib/postgresql/data` para evitar pérdida de datos si se destruye el contenedor.

### 2. API Backend (`autocare_api`)
* **Dockerfile:** Python 3.12 Slim.
* **Puerto del Host:** `8000`.
* **Volumen de Código:** Mapea la carpeta local `./backend` hacia `/app` en modo de desarrollo.
* **Volumen de Imágenes:** Mapea `./media` hacia `/media_files` de forma persistente. Aquí es donde se almacenan las fotos subidas por los usuarios.

### 3. Frontend Web (`autocare_web`)
* **Dockerfile (Multi-Etapa):**
  1. **Etapa de Compilación:** Usa `node:22-alpine` para instalar las dependencias (`npm install`) y compilar la SPA de Vue (`npm run build`), generando los archivos de distribución en `/app/dist`.
  2. **Etapa de Producción:** Descarta la imagen pesada de Node.js y copia los archivos generados a una imagen ligera de `nginx:alpine` en la carpeta `/usr/share/nginx/html`.
* **Puerto del Host:** `8080` (redirigido al puerto `80` interno de Nginx).

---

## 🔒 Variables de Entorno (`.env`)

Crea un archivo `.env` en la raíz del proyecto para configurar las credenciales:
```env
USUARIO_BD=autocare_user
PASSWORD_BD=Autocare_secure_pass123
POSTGRES_DB=autocare_db

SECRET_KEY=MessiLoversGatusoOnlyFans20
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ADMIN_PASSWORD=adminpass
ADMIN_EMAIL=admin@autocare.com
ADMIN_FULLNAME="Admin AutoCare Pro"
ADMIN_ROLE=admin

MAIL_USERNAME=tu-correo@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion-de-google
MAIL_FROM=tu-correo@gmail.com
```

---

## 🛡️ Configuración del Proxy Inverso (Caddy)

Caddy en el servidor host redirige el tráfico HTTPS externo hacia los puertos de tus contenedores Docker y gestiona los certificados SSL automáticamente.

### Ejemplo de `Caddyfile` en `/etc/caddy/Caddyfile`:
```caddy
# Subdominio para la interfaz web (Vite/Nginx en puerto 8080)
autocare.devcodery.duckdns.org {
    reverse_proxy localhost:8080
}

# Subdominio para la API lógica (Uvicorn en puerto 8000)
api.devcodery.duckdns.org {
    reverse_proxy localhost:8000
}
```

Para aplicar los cambios en tu servidor:
```bash
sudo systemctl reload caddy
```

---

## 🚀 Comandos de Despliegue Rápido

1. **Construir y levantar la suite por primera vez:**
   ```bash
   docker-compose up --build -d
   ```
2. **Ver logs del backend en vivo:**
   ```bash
   docker logs -f autocare_api
   ```
3. **Detener la aplicación sin perder datos:**
   ```bash
   docker-compose down
   ```
4. **Reconstruir solo el frontend tras cambios de código:**
   ```bash
   docker-compose up -d --no-deps --build frontend
   ```
