<template>
  <div class="dashboard-wrapper">

    <header class="section-header cell-shaded">

      <h2 class="section-title">
        <i class="fa-solid fa-user-plus"></i> ALTA DE NUEVO PERSONAL
      </h2>
    </header>

    <main class="form-container">
      <form @submit.prevent="registrarUsuario" class="brutalist-form cell-shaded">
        
        <div class="input-group">
          <label>NOMBRE COMPLETO</label>
          <input type="text" v-model="formulario.nombre" class="brutalist-input" required placeholder="Ej: Carlos Sainz" />
        </div>

        <div class="input-group">
          <label>CORREO ELECTRÓNICO</label>
          <input type="email" v-model="formulario.email" class="brutalist-input" required placeholder="carlos@taller.com" />
        </div>

        <div class="input-group">
          <label>CONTRASEÑA PROVISIONAL</label>
          <input type="password" v-model="formulario.password" class="brutalist-input" required placeholder="********" />
        </div>

        <div class="input-group">
          <label>ROL EN EL SISTEMA</label>
          <select v-model="formulario.rol" class="brutalist-input brutalist-select" required>
            <option value="user">USUARIO (Estándar)</option>
            <option value="admin">ADMINISTRADOR (Acceso Total)</option>
          </select>
        </div>

        <div v-if="mensaje" :class="['mensaje-alerta', tipoMensaje]">
          {{ mensaje }}
        </div>

        <button type="submit" class="submit-btn cell-shaded" :disabled="cargando">
          <i class="fa-solid fa-bolt"></i> {{ cargando ? 'REGISTRANDO...' : 'CREAR USUARIO' }}
        </button>

      </form>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

// El estado del formulario
const formulario = ref({
  nombre: '',
  email: '',
  rol: 'user',
  password: ''
})

const cargando = ref(false)
const mensaje = ref('')
const tipoMensaje = ref('') // 'exito' o 'error'

const registrarUsuario = async () => {
  cargando.value = true
  mensaje.value = ''
  
  try {
    // Mandamos los datos al backend
    await api.post('/usuarios/', formulario.value)
    
    mensaje.value = `¡Usuario ${formulario.value.nombre} registrado con éxito!`
    tipoMensaje.value = 'exito'
    
    // Limpiamos el formulario
    formulario.value = { nombre: '', email: '', rol: 'user', password: ''}
    
  } catch (error) {
    console.error('Error al registrar usuario:', error)
    mensaje.value = error.response?.data?.detail || 'Error al conectar con el servidor.'
    tipoMensaje.value = 'error'
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.section-header {
  background: #ffcc00;
  padding: 15px 20px;
  margin-bottom: 30px;
  border: 4px solid #000;
}

.section-title {
  font-family: 'Bangers', cursive;
  font-size: 2.5rem;
  color: #000;
  margin: 0;
  letter-spacing: 2px;
}

.brutalist-form {
  background: #111;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 25px;
  border: 4px solid #fff;
  box-shadow: 8px 8px 0px #00e5ff;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  color: #00e5ff;
  font-family: 'Bangers', cursive;
  font-size: 1.3rem;
  letter-spacing: 1px;
}

.brutalist-input {
  background: #000;
  color: #fff;
  border: 3px solid #555;
  padding: 12px 15px;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem;
  outline: none;
  transition: border-color 0.2s;
}

.brutalist-input:focus {
  border-color: #ffcc00;
}

.brutalist-select {
  cursor: pointer;
  appearance: none; /* Quita la flecha por defecto fea del navegador */
}

.submit-btn {
  background: #ff00ff; /* Un rosa neón muy agresivo */
  color: #fff;
  font-family: 'Bangers', cursive;
  font-size: 1.8rem;
  padding: 15px;
  border: 4px solid #000;
  cursor: pointer;
  margin-top: 10px;
  transition: transform 0.1s, box-shadow 0.1s;
}

.submit-btn:hover:not(:disabled) {
  transform: translate(-3px, -3px);
  box-shadow: 6px 6px 0px #000;
}

.submit-btn:disabled {
  background: #555;
  cursor: not-allowed;
}

.mensaje-alerta {
  padding: 15px;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  text-align: center;
  border: 3px solid #000;
}

.exito {
  background: #00ff66;
  color: #000;
}

.error {
  background: #ff3333;
  color: #fff;
}
</style>