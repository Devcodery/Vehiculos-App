# 🚗 AutoCare Pro: Gestión de Mantenimiento Vehicular Multi-Usuario

AutoCare Pro es un ecosistema completo para la gestión técnica y telemetría de flotas vehiculares personales. Permite registrar las intervenciones mecánicas hechas a cada coche, catalogar los repuestos o insumos utilizados con su respectivo fabricante y referencia, estructurar planes de mantenimiento preventivo y recibir notificaciones periódicas vía Gmail en caso de que alguna revisión esté vencida o próxima a vencer.

---

## 🛠️ Stack Tecnológico

El proyecto está diseñado bajo una arquitectura de microservicios contenedorizados listos para su despliegue:

* **Backend:** ![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) **FastAPI** (ORM SQLModel que unifica SQLAlchemy + Pydantic).
* **Frontend:** ![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green?logo=vue.js) **Vue 3 (Composition API)** con **Vite** y estilos estructurados en **Vanilla CSS (Brutalismo Cyberpunk)**.
* **Base de Datos:** ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql) **PostgreSQL** para la persistencia de datos relacionales.
* **Orquestación y Despliegue:** ![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker) **Docker & Docker Compose**.
* **Reverse Proxy:** ![Caddy](https://img.shields.io/badge/Caddy-Web_Server-black?logo=caddy) **Caddy** (gestión automática de HTTPS y SSL en el host).

---

## 💾 Modelo de Entidades y Relaciones (DB Schema)

La base de datos relacional PostgreSQL está estructurada en base a las siguientes relaciones de cardinalidad:

```
  [User] 1 -------- N [Vehicle]
    1                   1
    |                   |
    |                   |
    N                   N
  [RevisionType] 1 -- N [Revision] N ----- M [Product]
                                     (RevisionProducts)
```

### Tablas del Ecosistema
1. **User:** Información de registro de los usuarios, contraseñas hasheadas con `bcrypt` y roles.
2. **Vehicle:** Datos del coche (matrícula como llave primaria, marca, modelo, alias, kilometraje actual y foto).
3. **Product:** Repuestos y consumibles (marca, nombre, referencia/código de barra, categoría e imagen).
4. **RevisionType:** Protocolos y pautas de intervalos (cada cuántos kilómetros y meses se debe revisar).
5. **Revision:** Intervención técnica real registrada en un vehículo (fecha, precio, kilometraje y notas).
6. **RevisionProducts:** Relación intermedia que registra cuántas unidades de cada producto se usaron en una revisión específica.
7. **ServiceAlert:** Registro de telemetría de alertas de servicios enviadas (para controlar la recurrencia de avisos semanales los lunes).

---

## 🧭 Referencia de Endpoints del Backend

Los enrutadores modulares dividen la lógica en base a sus responsabilidades:

### Autenticación (`/auth`)
* `POST /auth/token` - Autentica credenciales y emite el JWT.
* `POST /auth/register` - Registro público de nuevos usuarios en el sistema.

### Perfil y Gestión de Usuarios (`/usuarios`)
* `GET /usuarios/me` - Retorna los datos del perfil del usuario en sesión.
* `PATCH /usuarios/me` - Modifica los datos personales o la contraseña (hasheándola de forma segura).
* `GET /usuarios/` - Obtiene listado general de usuarios (Solo administradores).

### Garaje (`/vehiculos`)
* `POST /vehiculos/` - Añade un vehículo al garaje (permite subir imágenes).
* `GET /vehiculos/` - Obtiene todos los vehículos del usuario activo.
* `GET /vehiculos/{vehiculo_id}` - Retorna el expediente técnico de un vehículo en particular.
* `PATCH /vehiculos/{vehiculo_id}` - Modifica datos y actualiza la foto de un vehículo.

### Repuestos e Inventario (`/productos`)
* `POST /productos/` - Agrega un producto al catálogo.
* `GET /productos/` - Retorna la lista de productos disponibles.
* `PATCH /productos/{producto_id}` - Actualiza datos e imagen del producto.
* `DELETE /productos/{producto_id}` - Elimina un producto.

### Historial de Intervenciones (`/revisiones`)
* `POST /revisiones/` - Registra un servicio vinculando los materiales utilizados.
* `GET /revisiones/` - Obtiene el historial de revisiones del usuario actual.
* `POST /revisiones/tipos/` - Crea un tipo de protocolo de mantenimiento.
* `GET /revisiones/tipos/` - Lista todos los tipos de revisión registrados globalmente.
* `GET /revisiones/tipos/mis/` - Retorna los tipos creados específicamente por el usuario activo.
* `PATCH /revisiones/tipos/{tipo_revision_id}` - Actualiza un protocolo.
* `DELETE /revisiones/tipos/{tipo_revision_id}` - Elimina un protocolo.

---

## ✉️ Daemon de Alertas de Telemetría (Gmail)

El backend incorpora una tarea programada asíncrona (`start_alert_scheduler`) que se inicia junto con FastAPI y se ejecuta en segundo plano. Compara el kilometraje actual de cada coche contra su historial y los límites de los protocolos para emitir notificaciones:

* **Estado Amarillo (`PRÓXIMO`):** Si restan `1.500 km` o menos para un servicio. Envía un correo con la ficha técnica del coche y los kilómetros restantes.
* **Estado Rojo (`VENCIDO`):** Si restan `0 km` o menos. Se notifica de inmediato al cambiar el estado. Si persiste en rojo, se volverá a notificar únicamente los **Lunes** si ha transcurrido al menos una semana (6 días o más) desde el último aviso.
* **Reseteo Automático:** Al registrar una nueva revisión de ese tipo en el coche, el sistema elimina el registro de alerta de la base de datos, re-estableciendo el semáforo a verde (`AL DÍA`).

---

## 🚀 Despliegue en Producción y Red

Los puertos internos expuestos por Docker Compose son los siguientes:
* **Base de Datos PostgreSQL:** Puerto host `5444` (interno `5432`).
* **FastAPI API:** Puerto host `8000` (interno `8000`).
* **Vue Frontend:** Puerto host `8080` (interno `80`).

### Configuración del Caddyfile en el Servidor Host
Caddy se encarga de redirigir los subdominios de forma segura y cifrada (HTTPS):

```caddy
# Frontend Web
autocare.devcodery.duckdns.org {
    reverse_proxy localhost:8080
}

# API Backend
api.devcodery.duckdns.org {
    reverse_proxy localhost:8000
}
```
*Las carpetas multimedia de carga de archivos `/media_files` se configuran como un volumen persistente dentro de Docker Compose.*