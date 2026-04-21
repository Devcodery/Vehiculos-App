# 🚗 AutoCare Pro: Gestión de Mantenimiento Vehicular Multi-Usuario

AutoCare Pro es una plataforma integral diseñada para el seguimiento detallado del mantenimiento de flotas vehiculares personales. Este proyecto nace de la necesidad de centralizar el historial de servicios, permitiendo no solo recordar cuándo toca el cambio, sino qué producto específico se usó.

## 🛠️ Stack Tecnológico

Elegido por su equilibrio entre rendimiento y facilidad de despliegue en servidores Ubuntu 24.04:

* **Backend:** ![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) **FastAPI** (Uso de SQLAlchemy + Pydantic para una API robusta).
* **Frontend:** ![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green?logo=vue.js) **Vue 3** con **Vite** y **Tailwind CSS**.
* **Base de Datos:** ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql) **PostgreSQL** para la persistencia de datos relacionales.
* **Orquestación:** ![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker) **Docker & Docker Compose**.
* **Reverse Proxy:** ![Caddy](https://img.shields.io/badge/Caddy-Web_Server-black?logo=caddy) **Caddy** (gestión automática de SSL para el servidor).

## ✨ Funcionalidades Principales

### 👤 Gestión de Usuarios y Vehículos

* **Multi-usuario:** Cada usuario gestiona su propia cuenta y datos de forma aislada.
* **Multi-vehículo:** Soporte para añadir múltiples coches bajo un mismo perfil.
* **Kilometraje Dinámico:** Registro del kilometraje actual para cálculos de proximidad.

### 🔧 Control de Mantenimiento (Customizado)

* **Fluidos y Filtros:** Registro de aceite, refrigerante, líquido de frenos, transmisión y filtros (aire, polen, aceite, gasolina).
* **Mantenimiento Pesado:** Control de correa de distribución, bomba de agua y bujías.
* **Aditivos y Limpieza:** Registro de productos específicos como Ceratec (Liqui Moly), limpiadores de inyectores y motor.
* **Trazabilidad total:** Cada registro guarda:
  * Fecha y Kilometraje.
  * Marca del producto (ej. Liqui Moly, Castrol, Bosch).
  * Nombre del producto específico.

## 📂 Estructura del Proyecto

```
/autocare-pro
├── backend/              # FastAPI API (Lógica, Modelos, CRUD)
├── frontend/             # Vue.js Application (Vistas, Componentes)
├── docker-compose.yml    # Orquestación de servicios para desarrollo
├── docker-compose.prod.yml # Configuración optimizada para servidor
└── Caddyfile             # Configuración del servidor web en Ubuntu
```

## 🚀 Guía de Inicio (Desarrollo Local)

Para ejecutar este proyecto en tu laptop (Pop!_OS):

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/autocare-pro.git
   cd autocare-pro
   ```

2. Levanta la infraestructura:

   ```bash
   docker-compose up --build
   ```

3. Accede a las interfaces:
   * App Web: http://localhost:5173
   * API Docs (Swagger): http://localhost:8000/docs

## 👨‍💻 Notas Académicas (DAM)

Este proyecto implementa patrones clave del ciclo formativo:

* **Normalización de DB:** Relaciones 1:N entre Usuarios-Vehículos y Vehículos-Registros.
* **Arquitectura de Microservicios:** Separación clara entre Front, Back y DB mediante contenedores.
* **Seguridad:** Implementación de hashing para contraseñas y (próximamente) JWT para sesiones.