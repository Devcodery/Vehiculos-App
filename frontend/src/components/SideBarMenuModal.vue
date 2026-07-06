<template>
    <div v-if="show" class="sidebar-overlay" @click="cerrar"></div>

    <aside :class="['brutalist-sidebar cell-shaded', { 'is-open': show }]">
        <div class="sidebar-header">
            <h2>MENÚ PRINCIPAL</h2>
            <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
        </div>

        <nav class="sidebar-nav">
            <button @click="navegarA('Home')" class="nav-item">
                <i class="fa-solid fa-warehouse"></i> Mi Garaje
            </button>
            <button @click="navegarA('MiCuenta')" class="nav-item">
                <i class="fa-solid fa-circle-user"></i> Mi Cuenta
            </button>
            <button v-if="authStore.user?.rol === 'admin'" @click="navegarA('RegistroUsuarios')" class="nav-item">
                <i class="fa-solid fa-user-plus"></i> Alta de Usuario
            </button>
            <button @click="navegarA('ListaProductos')" class="nav-item">
                <i class="fa-solid fa-box-open"></i> Catálogo de Productos
            </button>
            <button @click="navegarA('HistorialServicios')" class="nav-item">
                <i class="fa-solid fa-wrench"></i> Historial de Servicios
            </button>
            <button @click="navegarA('TiposServicio')" class="nav-item">
                <i class="fa-solid fa-tags"></i> Tipos de Servicio
            </button>
        </nav>

        <div class="sidebar-footer">
            <button @click="ejecutarLogout" class="nav-item logout-btn">
                <i class="fa-solid fa-right-from-bracket"></i> Cerrar Sesión
            </button>
        </div>
    </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
    show: Boolean
})

const emit = defineEmits(['close'])

const router = useRouter()
const authStore = useAuthStore()

const cerrar = () => {
    emit('close')
}

const navegarA = (nombreRuta) => {
    console.log(`Navegando a: ${nombreRuta}`)
    cerrar()
    router.push({ name: nombreRuta })
}

const ejecutarLogout = () => {
    cerrar()
    authStore.logout()
    router.push('/login')
}
</script>

<style scoped>
/* Fondo oscuro detrás del menú */
.sidebar-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(3px);
    z-index: 1000;
}

/* El panel lateral */
.brutalist-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    height: 100vh;
    background: #1a1a1a;
    border-right: 6px solid #ff00ff;
    z-index: 1001;
    display: flex;
    flex-direction: column;

    /* Animación de entrada: escondido a la izquierda */
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Cuando show es true, esta clase empuja el menú hacia la pantalla */
.brutalist-sidebar.is-open {
    transform: translateX(0);
}

.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background: #ff00ff;
    border-bottom: 4px solid #000;
}

.sidebar-header h2 {
    margin: 0;
    color: #000;
    font-family: 'Bangers', cursive;
    font-size: 1.8rem;
}

.close-btn {
    background: transparent;
    border: none;
    font-size: 2rem;
    color: #000;
    cursor: pointer;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    padding: 20px;
    gap: 15px;
    flex-grow: 1;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 15px;
    background: #000;
    color: #fff;
    border: 3px solid #555;
    padding: 12px 15px;
    font-family: 'Orbitron', sans-serif;
    font-size: 1rem;
    font-weight: bold;
    text-transform: uppercase;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
}

.nav-item i {
    color: #00e5ff;
    font-size: 1.2rem;
}

.nav-item:hover {
    background: #00e5ff;
    color: #000;
    border-color: #000;
    transform: translateX(10px);
}

.nav-item:hover i {
    color: #000;
}

.sidebar-footer {
    padding: 20px;
}

.logout-btn {
    background: #ff3333;
    color: #000;
    border-color: #000;
    width: 100%;
}

.logout-btn i {
    color: #000;
}

.logout-btn:hover {
    background: #cc0000;
    color: #fff;
}
</style>