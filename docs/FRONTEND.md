# 🎨 Arquitectura y Diseño del Frontend (Vue 3)

El frontend de **AutoCare Pro** es una Single Page Application (SPA) construida sobre **Vue 3** y empaquetada con **Vite**. Cuenta con estilos personalizados en CSS puro bajo un concepto visual **Brutalista Cyberpunk**.

---

## 📂 Estructura del Frontend
```
/frontend
├── src/
│   ├── main.js         # Punto de entrada de la aplicación Vue
│   ├── App.vue          # Componente raíz (Header, barra lateral y vistas)
│   ├── router/          # Configuración del enrutamiento y guardas
│   │   └── index.js
│   ├── stores/          # Gestión de estados compartidos (Pinia)
│   │   └── auth.js      # Sesión de usuario
│   ├── services/        # Cliente Axios para llamadas al backend
│   │   └── api.js
│   ├── components/      # Componentes reutilizables (Modales de formulario)
│   │   ├── CarModal.vue            # Registrar auto
│   │   ├── ProductModal.vue        # Registrar producto
│   │   ├── EditProductModal.vue    # Editar producto
│   │   ├── ServiceModal.vue        # Registrar mantenimiento
│   │   ├── ServiceTypeModal.vue    # Registrar tipo de servicio
│   │   ├── EditServiceTypeModal.vue# Editar tipo de servicio
│   │   ├── SideBarMenuModal.vue    # Menú de navegación
│   │   └── UpdateKmModal.vue       # Actualizar kilometraje rápido
│   └── views/           # Vistas del enrutador principal
│       ├── HomeView.vue            # Garaje principal del usuario
│       ├── ListaProductosView.vue  # Catálogo e inventario de piezas
│       ├── ServiciosView.vue       # Historial de intervenciones con filtros
│       ├── TipoServicioView.vue    # Lista de mantenimiento programado
│       ├── VehiculoDetalleView.vue # Ficha técnica, telemetría y tabla de servicios
│       ├── LoginView.vue           # Pantalla de acceso
│       ├── MiCuentaView.vue        # Edición de perfil y contraseñas
│       └── RegistroUsuariosView.vue# Registro de nuevos pilotos
```

---

## ⚙️ Componentes Clave

### 1. Cliente API de Axios (`services/api.js`)
Configura las llamadas de red unificadas hacia el backend:
* **`baseURL`:** Lee `import.meta.env.VITE_API_URL` en producción y cae en `http://localhost:8000` en desarrollo local.
* **Interceptor de Peticiones:** Intercepta cada llamada saliente e inyecta el encabezado `Authorization: Bearer <token>` de forma automática si existe una sesión activa guardada en el `localStorage`.
* **Interceptor de Respuestas:** Si el servidor responde con un código de estado `401 Unauthorized` (sesión expirada o token inválido), remueve automáticamente el token del almacenamiento local y redirige al usuario a la vista `/login`.

### 2. Enrutamiento y Guardas (`router/index.js`)
* Configura la navegación de la SPA a través de `vue-router`.
* **Rutas Privadas (`requiresAuth: true`):** El guarda global `router.beforeEach` intercepta la navegación. Si el usuario no está logueado, interrumpe el acceso y redirige a `/login`.
* **Rutas de Admin (`requiresAdmin: true`):** Bloquea las vistas especiales de administración (como el registro de nuevos pilotos) y retorna al usuario común al Home.
* **Limpieza de Consola:** Cumple con la especificación de Vue Router 4, retornando directamente el string del destino deseado (`return '/login'`) en lugar de usar parámetros `next()`.

### 3. Gestión de Sesiones con Pinia (`stores/auth.js`)
* Almacena de forma reactiva la información del usuario autenticado (nombre, email, rol, ID).
* Expone estados útiles en toda la interfaz como `isAuthenticated`.

---

## ⚡ Estilo Visual Brutalista Cyberpunk
Los componentes y vistas heredan una estética retro-futurista dura basada en las siguientes reglas CSS unificadas:

1. **Paleta Cromática Neón:**
   * Fondo oscuro rígido: `#111` / `#000`
   * Colores de realce neón: `#ff00ff` (morado/magenta neón) para botones principales y bordes de modales, `#00e5ff` (cyan) para etiquetas y textos destacados, `#00ff66` (verde neón) para valores y precios aprobados.
2. **Efecto Sombreado Brutalista (`cell-shaded`):**
   * Los botones, tarjetas y modales cuentan con bordes negros sólidos gruesos (`border: 3px solid #000;`) y sombras planas desplazadas sin degradado:
     ```css
     box-shadow: 4px 4px 0 #000;
     ```
3. **Tipografía:**
   * Títulos principales y etiquetas (`label`): Fuente cursiva de estilo cómic `'Bangers'`.
   * Textos informativos y valores técnicos: Fuente cuadriculada tecnológica `'Orbitron'` o sans-serif limpia para lectura regular.
4. **Ciclo de Vida de los Modales:**
   * Todos los modales se cargan en el DOM mediante directivas de Vue `v-if` a nivel de componente padre (en lugar de manipular clases de visibilidad CSS). Esto garantiza que, al cerrar el modal, este se destruya del DOM liberando memoria y reseteando limpiamente los estados internos del formulario para su próxima apertura.
