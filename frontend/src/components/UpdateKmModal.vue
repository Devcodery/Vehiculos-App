<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content cell-shaded">
      
      <header class="modal-header">
        <h2 class="modal-title"><i class="fa-solid fa-gauge-high"></i> ACTUALIZAR KILÓMETROS</h2>
        <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
      </header>
      
      <p v-if="car" class="modal-subtitle">
        {{ car.marca }} {{ car.modelo }} <br>
        <span class="matricula-badge">{{ car.matricula }}</span>
      </p>

      <div class="input-group">
        <label>NUEVO KILOMETRAJE:</label>
        <div class="km-input-wrapper">
          <input 
            type="number" 
            v-model="nuevoKm" 
            class="brutalist-input" 
            @keyup.enter="guardar"
          />
          <span class="km-label">KM</span>
        </div>
      </div>

      <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>

      <div class="modal-actions">
        <button @click="cerrar" class="btn-cancel cell-shaded">CANCELAR</button>
        <button @click="guardar" class="btn-save cell-shaded">GUARDAR</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  car: Object
})

const emit = defineEmits(['close', 'save'])

const nuevoKm = ref(0)
const errorMsg = ref('')

watch(() => props.show, (isOpen) => {
  if (isOpen && props.car) {
    nuevoKm.value = props.car.kilometraje
    errorMsg.value = ''
  }
})

const cerrar = () => {
  emit('close')
}

const guardar = () => {
  if (nuevoKm.value <= props.car.kilometraje) {
    errorMsg.value = `Debe ser mayor al actual (${props.car.kilometraje} km)`
    return
  }
  emit('save', nuevoKm.value)
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
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #111 !important;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border: 4px solid #ff00ff !important;
  box-shadow: 12px 12px 0 #000, 0 0 30px rgba(255, 0, 255, 0.3) !important;
}

.modal-header {
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border-bottom: none;
  padding: 0;
  margin-bottom: 5px;
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

.modal-subtitle {
  color: #fff;
  text-align: center;
  margin: 0;
  font-size: 1.2rem;
}

.matricula-badge {
  display: inline-block;
  background: #fff;
  color: #000;
  padding: 2px 8px;
  font-weight: bold;
  margin-top: 5px;
}

label, .input-group label {
  color: #00e5ff !important;
  font-family: 'Bangers', cursive !important;
  font-size: 1.2rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
}

.km-input-wrapper {
  display: flex;
  align-items: center;
  background: #000 !important;
  border: 2px solid #fff !important;
  margin-top: 5px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.km-input-wrapper:focus-within {
  border-color: #00e5ff !important;
}

.brutalist-input {
  flex-grow: 1;
  background: transparent !important;
  color: #fff !important;
  border: none !important;
  padding: 10px 12px !important;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.5rem;
  outline: none !important;
}

.km-label {
  color: #555;
  font-family: 'Bangers', cursive;
  font-size: 1.5rem;
  padding: 0 15px;
}

.error-text {
  color: #ff3333;
  font-weight: bold;
  margin: 0;
  text-align: center;
}

.modal-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.btn-cancel, .btn-save {
  flex: 1;
  padding: 12px;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  cursor: pointer;
  border: 3px solid #000;
}

.btn-cancel {
  background: #ccc;
  color: #000;
}

.btn-save {
  background: #00e5ff;
  color: #000;
}

.btn-cancel:hover, .btn-save:hover {
  transform: translate(-2px, -2px);
  box-shadow: 4px 4px 0 #000;
}
</style>