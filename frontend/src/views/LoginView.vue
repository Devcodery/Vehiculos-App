<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h1>Entrar a AutoCare</h1>
      
      <div class="input-group">
        <label>Email:</label>
        <input v-model="email" type="email" required placeholder="tu@email.com" />
      </div>

      <div class="input-group">
        <label>Contraseña:</label>
        <input v-model="password" type="password" required placeholder="••••••••"/>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Entrando...' : 'Iniciar Sesión' }}
      </button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

// 1. Variables reactivas (lo que escribes en los cuadros)
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const authStore = useAuthStore()
const router = useRouter()

// 2. La función que se ejecuta al dar click al botón
const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  // Llamamos a la "acción" de la Store que creamos antes
  const result = await authStore.login(email.value, password.value)

  if (result.success) {
    // Si sale bien, nos vamos a la Home
    router.push('/')
  } else {
    // Si sale mal, mostramos el error
    errorMessage.value = result.error
  }
  loading.value = false
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}
.login-form {
  background: #f4f4f4;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 300px;
}
.input-group {
  margin-bottom: 1rem;
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
}
.error {
  color: red;
  font-size: 0.9rem;
  margin-top: 10px;
}
</style>