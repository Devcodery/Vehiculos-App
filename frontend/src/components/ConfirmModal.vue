<template>
  <div v-if="show" class="modal-overlay" @click.self="cerrar">
    <div class="modal-content cell-shaded">
      <header class="modal-header">
        <h2 class="modal-title">
          <i class="fa-solid fa-triangle-exclamation modal-icon"></i>
          {{ titulo || '¿CONFIRMAR ACCIÓN?' }}
        </h2>
        <button @click="cerrar" class="close-btn" aria-label="Cerrar">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </header>

      <div class="modal-body">
        <div v-if="car" class="car-badge-preview cell-shaded-inner">
          <div class="car-details">
            <span class="car-name">{{ car.marca }} {{ car.modelo }}</span>
            <span v-if="car.alias" class="car-alias">"{{ car.alias }}"</span>
            <span class="car-plate"><i class="fa-solid fa-id-card"></i> Matrícula: <strong>{{ car.matricula }}</strong></span>
          </div>
        </div>

        <p class="modal-mensaje">{{ mensaje }}</p>

        <div v-if="advertencia" class="warning-box">
          <i class="fa-solid fa-fire-flame-curved"></i>
          <span>{{ advertencia }}</span>
        </div>
      </div>

      <div class="modal-actions">
        <button @click="cerrar" class="btn-cancel cell-shaded" :disabled="loading">
          <i class="fa-solid fa-xmark"></i> CANCELAR
        </button>

        <button @click="confirmar" class="btn-confirm cell-shaded" :disabled="loading">
          <i class="fa-solid" :class="loading ? 'fa-spinner fa-spin' : 'fa-trash-can'"></i>
          {{ loading ? 'ELIMINANDO...' : (textoConfirmar || 'ELIMINAR') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: { type: Boolean, default: false },
  titulo: { type: String, default: '¿ELIMINAR VEHÍCULO?' },
  mensaje: { type: String, default: '¿Estás seguro de que deseas eliminar este vehículo?' },
  advertencia: { type: String, default: 'Esta acción borrará permanentemente sus historiales de servicio y alertas.' },
  textoConfirmar: { type: String, default: 'SÍ, ELIMINAR' },
  car: { type: Object, default: null },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'confirm'])

const cerrar = () => {
  if (!props.loading) {
    emit('close')
  }
}

const confirmar = () => {
  emit('confirm')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: #111 !important;
  padding: 30px;
  width: 90%;
  max-width: 450px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border: 4px solid #ff3366 !important;
  box-shadow: 12px 12px 0 #000, 0 0 35px rgba(255, 51, 102, 0.4) !important;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.modal-title {
  font-family: 'Bangers', cursive;
  color: #ff3366;
  font-size: 1.9rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  letter-spacing: 1px;
  text-shadow: 2px 2px 0 #000;
}

.modal-icon {
  font-size: 1.8rem;
  color: #ffcc00;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 2rem;
  color: #888;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #ff3366;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.car-badge-preview {
  background: rgba(0, 0, 0, 0.6);
  border: 2px dashed #ff3366;
  padding: 12px 15px;
}

.car-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.car-name {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.2rem;
  font-weight: bold;
  color: #00e5ff;
}

.car-alias {
  font-style: italic;
  color: #ffcc00;
  font-size: 0.95rem;
}

.car-plate {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
  color: #aaa;
}

.car-plate strong {
  color: #fff;
}

.modal-mensaje {
  color: #fff;
  font-family: 'Roboto', sans-serif;
  font-size: 1.05rem;
  margin: 0;
  line-height: 1.5;
}

.warning-box {
  background: rgba(255, 51, 102, 0.15);
  border: 2px solid #ff3366;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ff6688;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.85rem;
  font-weight: bold;
}

.modal-actions {
  display: flex;
  gap: 15px;
  margin-top: 5px;
}

.btn-cancel, .btn-confirm {
  flex: 1;
  padding: 12px;
  font-family: 'Bangers', cursive;
  font-size: 1.3rem;
  cursor: pointer;
  border: 3px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: transform 0.1s, box-shadow 0.1s;
}

.btn-cancel {
  background: #333;
  color: #fff;
}

.btn-confirm {
  background: #ff3366;
  color: #fff;
}

.btn-cancel:hover:not(:disabled), .btn-confirm:hover:not(:disabled) {
  transform: translate(-3px, -3px);
  box-shadow: 4px 4px 0 #000;
}

.btn-confirm:hover:not(:disabled) {
  background: #ff0044;
}

.btn-confirm:disabled, .btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
