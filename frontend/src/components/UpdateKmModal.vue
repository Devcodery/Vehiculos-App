<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content cell-shaded">
      <h3 class="modal-title">ACTUALIZAR KILÓMETROS</h3>
      
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

// Cuando el modal se abre, rellenamos el input con el KM actual del coche
watch(() => props.show, (isOpen) => {
  if (isOpen && props.car) {
    nuevoKm.value = props.car.kilometraje
    errorMsg.value = '' // Limpiamos errores anteriores
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
  // Enviamos el dato a HomeView para que haga la petición a FastAPI
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
  background: #111;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border: 4px solid #fff;
  box-shadow: 8px 8px 0px #ffcc00;
}

.modal-title {
  font-family: 'Bangers', cursive;
  font-size: 2rem;
  color: #ffcc00;
  margin: 0;
  text-align: center;
  letter-spacing: 2px;
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

.input-group label {
  color: #00e5ff;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  letter-spacing: 1px;
}

.km-input-wrapper {
  display: flex;
  align-items: center;
  background: #000;
  border: 3px solid #555;
  margin-top: 5px;
}

.brutalist-input {
  flex-grow: 1;
  background: transparent;
  color: #00e5ff;
  border: none;
  padding: 10px;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.5rem;
  outline: none;
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