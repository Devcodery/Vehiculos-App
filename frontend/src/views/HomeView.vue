<template>
  <div class="home">
    <h1>Bienvenido a AutoCare</h1>
    <p>Si ves esto, es que has logrado entrar con tu Token.</p>
    <button @click="handleLogout">Cerrar Sesión</button>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.home {
  padding: 2rem;
  text-align: center;
}
button {
  margin-top: 1rem;
  padding: 10px 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>