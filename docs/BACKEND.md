# 🖥️ Arquitectura y Funcionamiento del Backend (FastAPI)

El backend de **AutoCare Pro** está programado en **Python 3.12** utilizando **FastAPI**. Destaca por su alta velocidad de ejecución, tipado estático obligatorio y generación automática de la documentación de endpoints a través de Swagger.

---

## 📂 Estructura del Backend
```
/backend
├── database.py         # Configuración del motor y sesiones de BD
├── main.py             # Punto de entrada de la aplicación (Lifespan, Middlewares)
├── models.py           # Modelos de datos unificados (SQLModel)
├── security.py         # Hashing, lógica de tokens JWT y dependencias OAuth2
├── routers/            # Controladores segmentados por recursos
│   ├── auth.py         # Login y registro de usuarios
│   ├── users.py        # Perfil y roles
│   ├── vehicles.py     # Garaje y fichas de vehículos
│   ├── products.py     # Inventario de repuestos
│   └── revision.py     # Registro de mantenimiento mecánico
└── services/           # Lógica en segundo plano
    ├── alert_scheduler.py # Hilo de monitoreo y envío de correos
    └── email_services.py  # Motor de comunicación SMTP (FastMail)
```

---

## ⚙️ Componentes Clave

### 1. Inicialización y Middleware (`main.py`)
Es el núcleo central de la aplicación. Se encarga de:
* **Lifespan Context:** Al iniciar, crea las tablas en PostgreSQL e inicia la tarea asíncrona de alertas en segundo plano. Si la base de datos está vacía, crea un usuario `Administrador` por defecto usando variables del entorno.
* **CORS Middleware:** Regula los accesos permitiendo peticiones cruzadas originadas en el servidor de desarrollo local o el dominio HTTPS de producción.
* **Archivos Estáticos:** Monta la carpeta `/media_files` bajo el prefijo de URL `/media` para servir de forma pública las imágenes de los vehículos y productos subidos por los usuarios.

### 2. Base de Datos (`database.py`)
Utiliza **SQLModel** (que combina SQLAlchemy y Pydantic) para interactuar con la base de datos PostgreSQL:
* **`engine`:** Administra el pool de conexiones hacia PostgreSQL usando la URL de conexión del entorno.
* **`get_session()`:** Generador de dependencias (*dependency injection*) que abre una sesión de base de datos en cada petición y la cierra automáticamente al terminar la transacción.

### 3. Seguridad y Control de Acceso (`security.py`)
* **Hasheo de Contraseñas:** Utiliza la librería `passlib` con el algoritmo `bcrypt` para cifrar las contraseñas.
* **JSON Web Tokens (JWT):** Genera tokens firmados criptográficamente mediante algoritmo `HS256` que expiran en 30 minutos.
* **`get_current_user`:** Dependencia inyectable en las rutas privadas que lee la cabecera `Authorization: Bearer <token>`, valida la firma, expira la sesión si el tiempo concluyó, y extrae el registro completo del usuario desde la base de datos.

### 4. Modelos Unificados (`models.py`)
La declaración de las entidades hereda de `SQLModel, table=True` para funcionar simultáneamente como validadores de entrada y tablas de base de datos:
* **Relación 1:N (Usuario - Vehículos):** El campo `user_id` en `Vehicle` asocia de forma rígida cada unidad a su conductor.
* **Relación Ternaria N:M (Revisión - Producto):** Las revisiones se enlazan con tipos de revisiones y, a su vez, contienen una relación intermedia (`RevisionProducts`) que mapea la cantidad exacta consumida de cada pieza de repuesto.

---

## 🚀 Pautas para el Desarrollador (Backend)
Al agregar un nuevo endpoint o característica, sigue estas directrices:
1. **Inyección de Sesiones:** Asegúrate de incluir `session: Session = Depends(get_session)` en los parámetros de la función del endpoint.
2. **Protección de Rutas:** Agrega `current_user: User = Depends(get_current_user)` para requerir que el usuario esté autenticado.
3. **Formularios con Archivos:** Si el endpoint maneja archivos adjuntos (como fotos), los parámetros textuales deben venir definidos como `Form(...)` en lugar de objetos JSON para que el navegador los envíe de forma conjunta con la petición multipart.
