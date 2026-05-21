<template>
  <Transition name="modal-fade">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content cell-shaded">
        
        <h2 class="modal-title">
          <i class="fa-solid fa-car"></i> REGISTRAR AUTO
        </h2>
        
        <form @submit.prevent="saveCar" class="comic-form">
          <div class="form-grid">
            <div class="input-group">
              <label class="label-form" for="marca">Marca</label>
              <input class="input-form" id="marca" v-model="carForm.marca" type="text" required placeholder="Ej: Nissan">
            </div>

            <div class="input-group">
              <label class="label-form" for="modelo">Modelo</label>
              <input class="input-form"  id="modelo" v-model="carForm.modelo" type="text" required placeholder="Ej: Skyline R34">
            </div>

            <div class="input-group">
              <label class="label-form" for="matricula">Matrícula</label>
              <input class="input-form"  id="matricula" v-model="carForm.matricula" type="text" required placeholder="Ej: GTR-001">
            </div>

            <div class="input-group">
              <label class="label-form" for="kilometraje">Kilometraje</label>
              <input class="input-form" id="kilometraje" v-model="carForm.kilometraje" type="number" required min="0" placeholder="Ej: 15000">
            </div>

            <div class="input-group">
              <label class="label-form" for="alias">Alias</label>
              <input class="input-form" id="alias" v-model="carForm.alias" type="text" placeholder="Ej: Godzilla">
            </div>
          </div>

          <div class="input-group upload-group">
            <label class="label-form" for="foto">Foto del Vehículo</label>
            <input id="foto" type="file" @change="handleFileUpload" accept="image/*" class="file-input cell-shaded">
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn cell-shaded" @click="$emit('close')">
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

// Definimos las señales que este componente puede enviar a su "padre" (HomeView)
const emit = defineEmits(['close', 'refreshGarage'])

const carForm = ref({
  marca: '',
  modelo: '',
  matricula: '',
  kilometraje: 0,
  alias: '',
  foto: null
})

// Controlamos el subir una imagen
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    carForm.value.foto = file
  }
}

const saveCar = async () => {
  try {
    const formData = new FormData()
    formData.append('marca', carForm.value.marca)
    formData.append('modelo', carForm.value.modelo)
    formData.append('matricula', carForm.value.matricula)
    formData.append('kilometraje', carForm.value.kilometraje)
    formData.append('alias', carForm.value.alias || "")
    
    if (carForm.value.foto) {
      formData.append('archivo_foto', carForm.value.foto)
    }

    await api.post('/vehiculos/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // Si sale bien, avisamos a HomeView para que recargue los coches y cierre el modal
    emit('refreshGarage')
    emit('close')

  } catch (error) {
    console.error("Error al guardar el coche:", error)
    alert("Hubo un error al guardar el vehículo. Revisa la consola.")
  }
}
</script>

<style scoped>
/* Pegamos aquí todos los estilos del modal que hicimos en el paso anterior */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: var(--panel-bg); padding: 30px; width: 90%; max-width: 500px;
  border: 5px solid var(--neon-blue); box-shadow: 12px 12px 0 #000, 0 0 30px rgba(0, 204, 255, 0.3);
}
.modal-title {
  font-family: 'Orbitron', sans-serif; color: var(--neon-blue); font-size: 1.8rem;
  margin-top: 0; margin-bottom: 25px; text-align: center;
  -webkit-text-stroke: 1px #000; text-shadow: 2px 2px 0 #000;
}
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.upload-group { margin-top: 15px; grid-column: 1 / -1; }
.file-input {
  background: #111; color: #fff; padding: 10px; border: 3px solid #000;
  width: 100%; cursor: pointer; font-family: 'Roboto', sans-serif;
}
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }
.cancel-btn, .save-btn {
  font-family: 'Bangers', cursive; font-size: 1.2rem; padding: 10px 20px;
  cursor: pointer; transition: transform 0.2s;
}
.cancel-btn { background: #ff3366; color: #fff; }
.save-btn { background: var(--neon-green); color: #e4d1d1; }
.cancel-btn:hover, .save-btn:hover { transform: translate(-3px, -3px); }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }
.input-group{
    display: grid;
    margin: 0.5em;
}

.label-form{
    margin: 0.35em;
}

.input-form{
    padding: 0.4em;
    background: #111;
    color: #ffffff;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Para Firefox */
input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}
</style>