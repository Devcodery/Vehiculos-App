<template>
  <Transition name="modal-fade">
    <div class="modal-overlay" @click.self="cerrar">
      <div class="modal-content cell-shaded">
        
        <header class="modal-header">
          <h2 class="modal-title"><i class="fa-solid fa-clipboard-check"></i> REGISTRAR TIPO SERVICIO</h2>
          <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
        </header>
        
        <form @submit.prevent="saveService" class="comic-form">
          <div class="form-grid">
            
            <div class="input-group">
              <label for="nombre_tipo_servicio" class="label-form">Nombre del Servicio:</label>
              <input id="nombre_tipo_servicio" v-model="serviceTypeForm.nombre" type="text" class="input-form" required placeholder="Ej: Cambio de Aceite">
            </div>

            <div class="input-group">
              <label for="cada_cuantos_km_tipo_servicio" class="label-form">Cada cuantos kilometros:</label>
              <input id="cada_cuantos_tipo_km_servicio" v-model="serviceTypeForm.cada_cuantos_Km" type="number" class="input-form" required min="0" placeholder="Ej: 10000">
            </div>
            
            <div class="input-group">
              <label for="cada_cuantos_meses_tipo_servicio" class="label-form">Cada cuantos meses:</label>
              <input id="cada_cuantos_meses_tipo_servicio" v-model="serviceTypeForm.cada_cuantos_Meses" type="number" class="input-form" required min="0" placeholder="Ej: 12">
            </div>

            <div class="input-group" style="grid-column: 1 / -1;">
              <label for="detalle_tipo_servicio" class="label-form">Detalles:</label>
              <textarea id="detalle_tipo_servicio" v-model="serviceTypeForm.detalles " rows="3" class="input-form" placeholder="Describe los detalles del mantenimiento o reparación..."></textarea>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn cell-shaded" @click="cerrar">
              CANCELAR
            </button>
            <button type="submit" class="save-btn cell-shaded">
              <i class="fa-solid fa-floppy-disk"></i> GUARDAR
            </button>
          </div>
        </form>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const emit = defineEmits(['close', 'refreshServices'])

const serviceTypeForm = ref({
  nombre: '',
  detalles: '',
  cada_cuantos_Km: '',
  cada_cuantos_Meses: '',
})

const cerrar = () => {
  emit('close')
}

const saveService = async () => {
  try {
    const payload = {
      nombre: serviceTypeForm.value.nombre,
      detalles: serviceTypeForm.value.detalles || '',
      cada_cuantos_Km: serviceTypeForm.value.cada_cuantos_Km,
      cada_cuantos_Meses: serviceTypeForm.value.cada_cuantos_Meses,
    }

    await api.post('/revisiones/tipos/', payload)

    emit('refreshServices')
    cerrar()

  } catch (error) {
    console.error("Error al guardar el tipo de servicio:", error)
    alert("Hubo un error al guardar el tipo de servicio. Revisa la consola.")
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: #111 !important; padding: 30px; width: 90%; max-width: 500px;
  border: 4px solid #ff00ff !important; box-shadow: 12px 12px 0 #000, 0 0 30px rgba(255, 0, 255, 0.3) !important;
}

.modal-header {
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border-bottom: none;
  padding: 0;
  margin-bottom: 25px;
  width: 100%;
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
  right: 0;
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

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }
.cancel-btn, .save-btn {
  font-family: 'Bangers', cursive; font-size: 1.2rem; padding: 10px 20px;
  cursor: pointer; transition: transform 0.2s;
}
.cancel-btn { background: #ff3366; color: #fff; border: 3px solid #000; }
.save-btn { background: var(--neon-pink); color: #000; border: 3px solid #000; }
.cancel-btn:hover, .save-btn:hover { transform: translate(-3px, -3px); }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }

/* --- TU DISEÑO DE CLASES --- */
.input-group {
    display: grid;
    margin: 0.5em;
}

label, .label-form {
    color: #00e5ff !important;
    font-family: 'Bangers', cursive !important;
    font-size: 1.2rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin: 0.35em;
}

.input-form {
    padding: 10px 12px !important;
    background: #000 !important;
    color: #ffffff !important;
    border: 2px solid #fff !important;
    outline: none !important;
    transition: border-color 0.2s ease;
}

.input-form:focus {
    border-color: #00e5ff !important;
}

textarea.input-form {
    resize: vertical;
    box-sizing: border-box;
    font-family: 'Roboto', sans-serif;
}
</style>