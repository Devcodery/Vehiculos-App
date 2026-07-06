<template>
  <div v-if="show" class="modal-overlay" @click="cerrar"></div>

  <div v-if="show" class="brutalist-modal cell-shaded">
    <header class="modal-header">
      <h2 class="modal-title"><i class="fa-solid fa-pen-to-square"></i> VER / EDITAR TIPO SERVICIO</h2>
      <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
    </header>

    <main class="modal-body">
      <form @submit.prevent="guardarCambios" class="modal-form">
        
        <div class="input-group">
          <label>Nombre del Servicio:</label>
          <input type="text" v-model="formulario.nombre" class="brutalist-input" required placeholder="Ej: Cambio de Aceite" />
        </div>

        <div class="two-fields">
          <div class="input-group">
            <label>Cada cuantos kilometros:</label>
            <input type="number" v-model="formulario.cada_cuantos_Km" class="brutalist-input" required min="0" placeholder="Ej: 10000" />
          </div>

          <div class="input-group">
            <label>Cada cuantos meses:</label>
            <input type="number" v-model="formulario.cada_cuantos_Meses" class="brutalist-input" required min="0" placeholder="Ej: 12" />
          </div>
        </div>

        <div class="input-group">
          <label>Detalles:</label>
          <textarea v-model="formulario.detalles" class="brutalist-input brutalist-textarea" rows="3" placeholder="Describe los detalles del mantenimiento..."></textarea>
        </div>

        <div v-if="mensaje" :class="['mensaje-alerta', tipoMensaje]">
          {{ mensaje }}
        </div>

        <div class="form-actions">
          <button type="submit" class="save-btn cell-shaded" :disabled="cargando">
            <i class="fa-solid fa-floppy-disk"></i> {{ cargando ? 'GUARDANDO...' : 'GUARDAR' }}
          </button>
          
          <button type="button" @click="eliminarTipo" class="delete-btn cell-shaded" :disabled="cargando">
            <i class="fa-solid fa-trash-can"></i> ELIMINAR
          </button>
        </div>

      </form>
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/services/api'

const props = defineProps({
  show: Boolean,
  tipoServicio: Object
})

const emit = defineEmits(['close', 'refresh'])

const formulario = ref({
  nombre: '',
  detalles: '',
  cada_cuantos_Km: 0,
  cada_cuantos_Meses: 0
})

const cargando = ref(false)
const mensaje = ref('')
const tipoMensaje = ref('')

watch(() => props.tipoServicio, (nuevoTipo) => {
  if (nuevoTipo) {
    formulario.value = { ...nuevoTipo }
  }
}, { immediate: true })

const cerrar = () => {
  mensaje.value = ''
  emit('close')
}

const guardarCambios = async () => {
  cargando.value = true
  mensaje.value = ''
  try {
    await api.patch(`/revisiones/tipos/${props.tipoServicio.tipo_revision_id}`, {
      nombre: formulario.value.nombre,
      detalles: formulario.value.detalles,
      cada_cuantos_Km: parseInt(formulario.value.cada_cuantos_Km),
      cada_cuantos_Meses: parseInt(formulario.value.cada_cuantos_Meses)
    })
    mensaje.value = '¡Tipo de servicio actualizado!'
    tipoMensaje.value = 'exito'
    emit('refresh')
    setTimeout(() => cerrar(), 1000)
  } catch (error) {
    mensaje.value = error.response?.data?.detail || 'Error al actualizar.'
    tipoMensaje.value = 'error'
  } finally {
    cargando.value = false
  }
}

const eliminarTipo = async () => {
  if (!confirm(`¿Seguro que deseas eliminar "${props.tipoServicio.nombre}" por completo?`)) return
  cargando.value = true
  try {
    await api.delete(`/revisiones/tipos/${props.tipoServicio.tipo_revision_id}`)
    emit('refresh')
    cerrar()
  } catch (error) {
    mensaje.value = error.response?.data?.detail || 'Error al eliminar.'
    tipoMensaje.value = 'error'
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  z-index: 1100;
}

.brutalist-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 550px;
  background: #111 !important;
  border: 4px solid #ff00ff !important;
  box-shadow: 12px 12px 0 #000, 0 0 30px rgba(255, 0, 255, 0.3) !important;
  z-index: 1101;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border-bottom: none;
  padding: 25px 25px 0 25px;
  width: 100%;
  box-sizing: border-box;
  position: relative;
}

.modal-title {
  font-family: 'Bangers', cursive;
  color: #ff00ff;
  font-size: 1.8rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: normal;
  -webkit-text-stroke: 1px #000;
  text-shadow: 2px 2px 0 #000;
}

.close-btn {
  position: absolute;
  right: 25px;
  background: transparent;
  border: none;
  font-size: 2rem;
  color: #fff;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #ff00ff;
}

.modal-body {
  padding: 25px;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.two-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

label, .input-group label {
  color: #00e5ff !important;
  font-family: 'Bangers', cursive !important;
  font-size: 1.2rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
}

.brutalist-input {
  background: #000 !important;
  color: #fff !important;
  border: 2px solid #fff !important;
  padding: 10px 12px !important;
  font-family: 'Orbitron', sans-serif;
  font-size: 1rem;
  outline: none !important;
  transition: border-color 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}
.brutalist-input:focus { border-color: #00e5ff !important; }

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.save-btn {
  flex: 2;
  background: #ff00ff !important;
  color: #000 !important;
  font-family: 'Bangers', cursive;
  font-size: 1.5rem;
  padding: 12px;
  border: 3px solid #000;
  cursor: pointer;
  transition: transform 0.1s;
}
.save-btn:hover:not(:disabled) { transform: translate(-2px, -2px); box-shadow: 4px 4px 0 #000; }

.delete-btn {
  flex: 1;
  background: #ff3333;
  color: #fff;
  font-family: 'Bangers', cursive;
  font-size: 1.5rem;
  padding: 12px;
  border: 3px solid #000;
  cursor: pointer;
  transition: transform 0.1s;
}
.delete-btn:hover:not(:disabled) { transform: translate(-2px, -2px); box-shadow: 4px 4px 0 #000; }

.save-btn:disabled, .delete-btn:disabled { background: #444; cursor: not-allowed; }

.mensaje-alerta {
  padding: 12px;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  text-align: center;
  border: 2px solid #000;
}
.exito { background: #00ff66; color: #000; }
.error { background: #ff3333; color: #fff; }

.brutalist-textarea {
  resize: vertical;
}
</style>
