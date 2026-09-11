<template>
  <div class="dashboard-wrapper">
    <header class="section-header cell-shaded">
      <div class="header-left">
        <h2 class="section-title">
          <i class="fa-solid fa-users-gear"></i> GESTIÓN DE USUARIOS
        </h2>
        <span class="admin-badge">ZONA ADMINISTRADOR</span>
      </div>

      <div class="header-actions">
        <button @click="cargarUsuarios" class="refresh-btn cell-shaded" :disabled="cargando" title="Recargar lista">
          <i class="fa-solid fa-arrows-rotate" :class="{ 'fa-spin': cargando }"></i>
        </button>
        <button @click="router.push({ name: 'RegistroUsuarios' })" class="add-btn cell-shaded">
          <i class="fa-solid fa-user-plus"></i> NUEVO USUARIO
        </button>
      </div>
    </header>

    <!-- Barra de Métricas -->
    <section class="stats-grid">
      <div class="stat-card cell-shaded">
        <div class="stat-icon"><i class="fa-solid fa-users"></i></div>
        <div class="stat-info">
          <span class="stat-label">TOTAL USUARIOS</span>
          <span class="stat-value">{{ usuarios.length }}</span>
        </div>
      </div>

      <div class="stat-card cell-shaded admin-stat">
        <div class="stat-icon"><i class="fa-solid fa-shield-halved"></i></div>
        <div class="stat-info">
          <span class="stat-label">ADMINISTRADORES</span>
          <span class="stat-value">{{ totalAdmins }}</span>
        </div>
      </div>

      <div class="stat-card cell-shaded user-stat">
        <div class="stat-icon"><i class="fa-solid fa-user-gear"></i></div>
        <div class="stat-info">
          <span class="stat-label">USUARIOS ESTÁNDAR</span>
          <span class="stat-value">{{ totalEstandar }}</span>
        </div>
      </div>
    </section>

    <!-- Barra de Filtros -->
    <section class="filters-bar cell-shaded">
      <div class="input-group search-group">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input
          type="text"
          v-model="filtroTexto"
          class="brutalist-input search-input"
          placeholder="Buscar por nombre o correo electrónico..."
        />
      </div>

      <div class="input-group select-group">
        <select v-model="filtroRol" class="brutalist-input select-input">
          <option value="TODOS">TODOS LOS ROLES</option>
          <option value="admin">SOLO ADMIN</option>
          <option value="usuario">SOLO USUARIO (ESTÁNDAR)</option>
        </select>
      </div>
    </section>

    <!-- Lista de Usuarios -->
    <main class="users-container">
      <div v-if="cargando && usuarios.length === 0" class="loading-state cell-shaded">
        <i class="fa-solid fa-circle-notch fa-spin"></i>
        <p>CARGANDO USUARIOS DEL SISTEMA...</p>
      </div>

      <div v-else-if="usuariosFiltrados.length === 0" class="empty-state cell-shaded">
        <i class="fa-solid fa-user-slash"></i>
        <p>No se encontraron usuarios con los criterios de búsqueda.</p>
      </div>

      <div v-else class="users-grid">
        <div
          v-for="u in usuariosFiltrados"
          :key="u.user_id"
          :class="['user-card cell-shaded', { 'is-current-user': esUsuarioActual(u) }]"
        >
          <div class="card-top">
            <span :class="['role-pill', u.rol === 'admin' ? 'pill-admin' : 'pill-user']">
              <i :class="u.rol === 'admin' ? 'fa-solid fa-shield' : 'fa-solid fa-user'"></i>
              {{ u.rol === 'admin' ? 'ADMIN' : 'USUARIO' }}
            </span>

            <span v-if="esUsuarioActual(u)" class="current-user-tag">
              <i class="fa-solid fa-circle-check"></i> TU CUENTA
            </span>

            <span class="user-id-tag">ID: #{{ u.user_id }}</span>
          </div>

          <div class="user-main-info">
            <div class="avatar-box cell-shaded-inner">
              <i :class="u.rol === 'admin' ? 'fa-solid fa-user-shield' : 'fa-solid fa-circle-user'"></i>
            </div>

            <div class="user-details">
              <h3 class="user-name">{{ u.nombre }}</h3>
              <p class="user-email">
                <i class="fa-solid fa-envelope"></i> {{ u.email }}
              </p>
            </div>
          </div>

          <div class="card-bottom">
            <button
              v-if="esUsuarioActual(u)"
              class="action-btn disabled-btn cell-shaded"
              disabled
              title="No puedes eliminar tu propia cuenta de administrador"
            >
              <i class="fa-solid fa-lock"></i> PROTEGIDO (SESIÓN ACTIVA)
            </button>

            <button
              v-else
              @click="abrirConfirmacionEliminar(u)"
              class="action-btn delete-btn cell-shaded"
              title="Eliminar usuario del sistema"
            >
              <i class="fa-solid fa-trash-can"></i> ELIMINAR USUARIO
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de Confirmación de Borrado -->
    <ConfirmModal
      :show="showConfirmModal"
      titulo="¿ELIMINAR USUARIO?"
      mensaje="¿Estás seguro de que deseas dar de baja a este usuario del sistema?"
      advertencia="¡ADVERTENCIA CRÍTICA! Se borrarán todos los vehículos asociados a este usuario, incluyendo sus revisiones y registros de alerta."
      textoConfirmar="SÍ, ELIMINAR USUARIO"
      :userItem="usuarioAEliminar"
      :loading="eliminando"
      @close="cerrarModal"
      @confirm="ejecutarEliminacion"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'
import ConfirmModal from '@/components/ConfirmModal.vue'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const usuarios = ref([])
const cargando = ref(false)
const filtroTexto = ref('')
const filtroRol = ref('TODOS')

const showConfirmModal = ref(false)
const usuarioAEliminar = ref(null)
const eliminando = ref(false)

const esUsuarioActual = (u) => {
  return u.user_id === authStore.user?.id || u.email === authStore.user?.email
}

const totalAdmins = computed(() => {
  return usuarios.value.filter((u) => u.rol === 'admin').length
})

const totalEstandar = computed(() => {
  return usuarios.value.filter((u) => u.rol !== 'admin').length
})

const usuariosFiltrados = computed(() => {
  return usuarios.value.filter((u) => {
    const texto = filtroTexto.value.trim().toLowerCase()
    const coincideTexto =
      !texto ||
      u.nombre.toLowerCase().includes(texto) ||
      u.email.toLowerCase().includes(texto)

    let coincideRol = true
    if (filtroRol.value === 'admin') {
      coincideRol = u.rol === 'admin'
    } else if (filtroRol.value === 'usuario') {
      coincideRol = u.rol !== 'admin'
    }

    return coincideTexto && coincideRol
  })
})

const cargarUsuarios = async () => {
  cargando.value = true
  try {
    const res = await api.get('/usuarios/')
    usuarios.value = res.data
  } catch (error) {
    console.error('Error al obtener lista de usuarios:', error)
    notificationStore.showError(
      error.response?.data?.detail || 'Error al cargar la lista de usuarios.'
    )
  } finally {
    cargando.value = false
  }
}

const abrirConfirmacionEliminar = (u) => {
  usuarioAEliminar.value = u
  showConfirmModal.value = true
}

const cerrarModal = () => {
  if (!eliminando.value) {
    showConfirmModal.value = false
    usuarioAEliminar.value = null
  }
}

const ejecutarEliminacion = async () => {
  if (!usuarioAEliminar.value) return

  eliminando.value = true
  try {
    const userId = usuarioAEliminar.value.user_id
    const userName = usuarioAEliminar.value.nombre
    await api.delete(`/usuarios/${userId}`)
    
    notificationStore.showSuccess(`Usuario "${userName}" eliminado correctamente.`)
    showConfirmModal.value = false
    usuarioAEliminar.value = null
    await cargarUsuarios()
  } catch (error) {
    console.error('Error al eliminar usuario:', error)
    notificationStore.showError(
      error.response?.data?.detail || 'No se pudo eliminar el usuario.'
    )
  } finally {
    eliminando.value = false
  }
}

onMounted(() => {
  cargarUsuarios()
})
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.section-header {
  background: #ffcc00;
  padding: 15px 25px;
  margin-bottom: 25px;
  border: 4px solid #000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.section-title {
  font-family: 'Bangers', cursive;
  font-size: 2.3rem;
  color: #000;
  margin: 0;
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-badge {
  background: #000;
  color: #ff00ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.8rem;
  font-weight: 900;
  padding: 4px 10px;
  border: 2px solid #000;
  letter-spacing: 1px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.refresh-btn {
  background: #000;
  color: #00e5ff;
  border: 3px solid #000;
  padding: 10px 14px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.1s, background-color 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  transform: translate(-2px, -2px);
  background: #222;
}

.add-btn {
  background: #00e5ff;
  color: #000;
  font-family: 'Bangers', cursive;
  font-size: 1.25rem;
  border: 3px solid #000;
  padding: 10px 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.1s;
}

.add-btn:hover {
  transform: translate(-3px, -3px);
  background: #33eeff;
}

/* Estadísticas */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  background: #111;
  border: 4px solid #fff;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  font-size: 2.2rem;
  color: #00e5ff;
}

.admin-stat .stat-icon {
  color: #ff00ff;
}

.user-stat .stat-icon {
  color: #ffcc00;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.85rem;
  color: #888;
  letter-spacing: 1px;
  font-weight: 700;
}

.stat-value {
  font-family: 'Bangers', cursive;
  font-size: 2.2rem;
  color: #fff;
  line-height: 1;
  margin-top: 4px;
}

/* Barra de Filtros */
.filters-bar {
  background: #111;
  border: 4px solid #fff;
  padding: 18px 20px;
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  align-items: center;
  position: relative;
}

.search-group {
  flex: 2;
  min-width: 250px;
}

.select-group {
  flex: 1;
  min-width: 200px;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: #888;
  font-size: 1.1rem;
}

.brutalist-input {
  background: #000;
  color: #fff;
  border: 3px solid #555;
  padding: 12px 15px;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.95rem;
  width: 100%;
  outline: none;
  transition: border-color 0.2s;
}

.search-input {
  padding-left: 42px;
}

.brutalist-input:focus {
  border-color: #ffcc00;
}

.select-input {
  cursor: pointer;
  appearance: none;
}

/* Grilla de Usuarios */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 25px;
}

.user-card {
  background: #111;
  border: 4px solid #fff;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  position: relative;
  transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
  transform: translate(-3px, -3px);
  box-shadow: 8px 8px 0px #00e5ff;
}

.user-card.is-current-user {
  border-color: #00ff66;
  box-shadow: 6px 6px 0px #00ff66;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  border-bottom: 2px dashed #444;
  padding-bottom: 12px;
}

.role-pill {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.75rem;
  font-weight: 900;
  padding: 4px 10px;
  border: 2px solid #000;
  display: flex;
  align-items: center;
  gap: 6px;
  letter-spacing: 1px;
}

.pill-admin {
  background: #ff00ff;
  color: #000;
}

.pill-user {
  background: #00e5ff;
  color: #000;
}

.current-user-tag {
  background: #00ff66;
  color: #000;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.75rem;
  font-weight: 900;
  padding: 3px 8px;
  border: 2px solid #000;
}

.user-id-tag {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.8rem;
  color: #777;
  font-weight: bold;
}

.user-main-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-box {
  width: 60px;
  height: 60px;
  background: #000;
  border: 3px solid #ffcc00;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.9rem;
  color: #ffcc00;
  flex-shrink: 0;
}

.user-card.is-current-user .avatar-box {
  border-color: #00ff66;
  color: #00ff66;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow: hidden;
}

.user-name {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.15rem;
  font-weight: 800;
  color: #fff;
  margin: 0;
  word-break: break-word;
}

.user-email {
  font-family: 'Roboto', sans-serif;
  font-size: 0.9rem;
  color: #aaa;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  word-break: break-all;
}

.user-email i {
  color: #ffcc00;
  font-size: 0.85rem;
}

.card-bottom {
  margin-top: auto;
  border-top: 2px dashed #444;
  padding-top: 14px;
}

.action-btn {
  width: 100%;
  padding: 12px;
  font-family: 'Bangers', cursive;
  font-size: 1.15rem;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  border: 3px solid #000;
  transition: transform 0.1s, background 0.2s;
}

.delete-btn {
  background: #ff3366;
  color: #fff;
}

.delete-btn:hover {
  background: #ff0044;
  transform: translate(-2px, -2px);
  box-shadow: 4px 4px 0 #000;
}

.disabled-btn {
  background: #252525;
  color: #00ff66;
  cursor: not-allowed;
  opacity: 0.9;
  border-color: #00ff66;
}

/* Estados Vacíos y Carga */
.loading-state,
.empty-state {
  background: #111;
  border: 4px solid #fff;
  padding: 40px 20px;
  text-align: center;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem;
}

.loading-state i,
.empty-state i {
  font-size: 3rem;
  color: #ffcc00;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
  }

  .add-btn {
    flex: 1;
    justify-content: center;
  }

  .filters-bar {
    flex-direction: column;
  }
}
</style>
