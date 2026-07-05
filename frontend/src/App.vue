<template>
  <template v-if="route.path !== '/login'">
    
    <header class="top-nav cell-shaded">
      <div class="nav-left">
        <button @click="showMenuModal = true" class="hamburger-btn">
          <i class="fa-solid fa-bars menu-icon"></i>
        </button>
      </div>
      <div class="nav-center">
        <h1 class="brand-title">AutoCare</h1>
      </div>
      <div class="nav-right">
        <button @click="handleLogout" class="logout-btn cell-shaded">
          SALIR <i class="fa-solid fa-power-off"></i>
        </button>
      </div>
    </header>

    <SidebarMenu :show="showMenuModal" @close="showMenuModal = false" />

  </template>

  <RouterView />
</template>

<script setup>
import { ref } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SidebarMenu from '@/components/SideBarMenuModal.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Control del menú lateral global
const showMenuModal = ref(false)

// Lógica de cerrar sesión global
const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
/* --- ESTILOS GLOBALES BÁSICOS --- */
body {
  font-family: sans-serif;
  margin: 0;
  padding: 0;
  background-color: #1a1a1a;
}

/* --- ESTILOS DE LA CABECERA GLOBAL --- */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #111; /* Asegura que coincida con tu var(--panel-bg) */
  padding: 15px 30px;
  border-bottom: 4px solid #fff;
}

.nav-left {
  display: flex;
  align-items: center;
}

.brand-title {
  font-family: 'Orbitron', sans-serif;
  font-style: italic;
  font-size: 3rem;
  color: #00e5ff; /* Tu cyan neón */
  margin: 0;
  -webkit-text-stroke: 1.5px #000;
  text-shadow: 3px 3px 0 #000;
}

.hamburger-btn {
  background: none;
  border: none;
  color: #00ff66;
  cursor: pointer;
  padding: 5px;
  transition: transform 0.2s;
}
.hamburger-btn:hover { transform: scale(1.1); }
.menu-icon { font-size: 35px; }

.logout-btn {
  background: #ff00ff; /* Rosa neón */
  color: #000;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  padding: 8px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 3px solid #000;
  transition: transform 0.2s;
}
.logout-btn:hover {
  transform: translate(-3px, -3px);
  box-shadow: 6px 6px 0 #000;
}
</style>