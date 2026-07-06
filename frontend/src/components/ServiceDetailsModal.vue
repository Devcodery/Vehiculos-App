<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content cell-shaded">
      
      <header class="modal-header">
        <h2 class="modal-title">
          <i class="fa-solid fa-file-invoice"></i> DETALLE DE SERVICIO
        </h2>
        <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
      </header>

      <div class="service-details-body" v-if="service">
        <!-- Main details badge -->
        <div class="main-info-grid">
          <div class="info-block cell-shaded-inner">
            <span class="info-label">TIPO DE SERVICIO</span>
            <span class="info-value service-type">{{ service.tipo_revision_nombre || 'Mantenimiento' }}</span>
          </div>

          <div class="info-block cell-shaded-inner">
            <span class="info-label">VEHÍCULO</span>
            <span class="info-value vehicle-id"><i class="fa-solid fa-car"></i> {{ service.vehiculo_id }}</span>
          </div>
        </div>

        <div class="secondary-info-grid">
          <div class="info-block cell-shaded-inner">
            <span class="info-label">KILOMETRAJE</span>
            <span class="info-value"><i class="fa-solid fa-gauge-high"></i> {{ service.kilometro_servicio }} km</span>
          </div>

          <div class="info-block cell-shaded-inner">
            <span class="info-label">FECHA</span>
            <span class="info-value"><i class="fa-regular fa-calendar"></i> {{ formatearFecha(service.fecha) }}</span>
          </div>

          <div class="info-block cell-shaded-inner cost-block">
            <span class="info-label">COSTO TOTAL</span>
            <span class="info-value highlight-green">{{ service.precio !== null ? service.precio + ' €' : 'N/A' }}</span>
          </div>
        </div>

        <!-- Notes / Observations Section -->
        <div class="detail-section">
          <h4 class="section-subtitle"><i class="fa-solid fa-comment-dots"></i> NOTAS / OBSERVACIONES</h4>
          <div class="notes-box">
            <p v-if="service.nota" class="notes-text">"{{ service.nota }}"</p>
            <p v-else class="notes-text empty-text">Sin notas registradas en esta intervención.</p>
          </div>
        </div>

        <!-- Products / Parts Used Section -->
        <div class="detail-section">
          <h4 class="section-subtitle"><i class="fa-solid fa-box-open"></i> MATERIALES / REUESTOS UTILIZADOS</h4>
          
          <div v-if="service.productos && service.productos.length > 0" class="products-list">
            <div v-for="prod in service.productos" :key="prod.producto_id" class="product-item cell-shaded-inner">
              <div class="product-header">
                <span class="product-brand">{{ prod.marca }}</span>
                <span class="product-qty">x{{ prod.cantidad }}</span>
              </div>
              <div class="product-name">{{ prod.nombre }}</div>
              <div class="product-meta">
                <span v-if="prod.referencia" class="product-ref"><i class="fa-solid fa-hashtag"></i> {{ prod.referencia }}</span>
                <span v-if="prod.categoria" class="product-cat"><i class="fa-solid fa-tags"></i> {{ prod.categoria }}</span>
              </div>
            </div>
          </div>

          <div v-else class="empty-products-box cell-shaded-inner">
            <i class="fa-solid fa-circle-info"></i> No se registraron repuestos o productos en este servicio.
          </div>
        </div>

      </div>

      <div class="modal-actions">
        <button @click="cerrar" class="btn-close cell-shaded">CERRAR</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  show: Boolean,
  service: Object
})

const emit = defineEmits(['close'])

const cerrar = () => {
  emit('close')
}

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return 'N/A'
  const date = new Date(fechaStr)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
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
  z-index: 1100;
}

.modal-content {
  background: #111 !important;
  padding: 30px;
  width: 95%;
  max-width: 550px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border: 4px solid #00ff66 !important;
  box-shadow: 12px 12px 0 #000, 0 0 35px rgba(0, 255, 102, 0.2) !important;
  overflow-y: auto;
}

/* Scrollbar for modal content */
.modal-content::-webkit-scrollbar {
  width: 8px;
}
.modal-content::-webkit-scrollbar-track {
  background: #111;
}
.modal-content::-webkit-scrollbar-thumb {
  background: #00ff66;
  border: 2px solid #111;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 3px solid #00ff66;
  padding-bottom: 12px;
}

.modal-title {
  font-family: 'Bangers', cursive;
  color: #00ff66;
  font-size: 2rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: normal;
  text-shadow: 2px 2px 0 #000;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.8rem;
  color: #fff;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #00ff66;
}

.service-details-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Grids for info */
.main-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.secondary-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1.2fr;
  gap: 15px;
}

@media (max-width: 480px) {
  .main-info-grid, .secondary-info-grid {
    grid-template-columns: 1fr;
  }
}

.cell-shaded-inner {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #333;
  padding: 10px 15px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-family: 'Bangers', cursive;
  font-size: 0.95rem;
  color: #888;
  letter-spacing: 0.5px;
}

.info-value {
  font-family: 'Orbitron', sans-serif;
  color: #fff;
  font-size: 1.1rem;
  font-weight: bold;
}

.service-type {
  color: #ff00ff;
  font-size: 1.2rem;
}

.vehicle-id {
  color: #00e5ff;
}

.highlight-green {
  color: #00ff66;
  font-size: 1.3rem;
}

.cost-block {
  border-color: #00ff66;
}

/* Section titles */
.detail-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-subtitle {
  font-family: 'Bangers', cursive;
  font-size: 1.25rem;
  color: #00e5ff;
  margin: 0;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Notes callout box */
.notes-box {
  background: rgba(0, 0, 0, 0.4);
  border-left: 4px solid #ffcc00;
  padding: 12px 15px;
}

.notes-text {
  font-family: 'Roboto', sans-serif;
  color: #ddd;
  font-style: italic;
  font-size: 1rem;
  line-height: 1.4;
  margin: 0;
}

.empty-text {
  color: #666;
}

/* Products styling */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 200px;
  overflow-y: auto;
  padding-right: 5px;
}

.products-list::-webkit-scrollbar {
  width: 5px;
}
.products-list::-webkit-scrollbar-thumb {
  background: #333;
}

.product-item {
  border-left: 3px solid #ff00ff;
  background: rgba(255, 0, 255, 0.02);
  gap: 6px;
  padding: 10px 12px;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-brand {
  font-family: 'Orbitron', sans-serif;
  color: #ff00ff;
  font-weight: bold;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.product-qty {
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  color: #00ff66;
}

.product-name {
  font-family: 'Roboto', sans-serif;
  color: #fff;
  font-weight: 500;
  font-size: 1rem;
}

.product-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #888;
}

.product-meta i {
  color: #555;
}

.empty-products-box {
  border: 2px dashed #444;
  text-align: center;
  padding: 15px;
  color: #777;
  font-family: 'Roboto', sans-serif;
  font-size: 0.95rem;
}

.empty-products-box i {
  margin-right: 5px;
}

/* Actions styling */
.modal-actions {
  display: flex;
  margin-top: 10px;
}

.btn-close {
  flex: 1;
  background: #333;
  color: #fff;
  border: 3px solid #000;
  font-family: 'Bangers', cursive;
  padding: 12px;
  font-size: 1.3rem;
  cursor: pointer;
  text-transform: uppercase;
  transition: transform 0.1s;
}

.btn-close:hover {
  background: #ff00ff;
  color: #000;
  transform: translate(-3px, -3px);
  box-shadow: 4px 4px 0 #000;
  border-color: #000;
}
</style>
