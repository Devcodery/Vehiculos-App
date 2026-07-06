<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content cell-shaded" :class="{ 'editing-mode': isEditing }">

      <header class="modal-header">
        <h2 class="modal-title">
          <i class="fa-solid" :class="isEditing ? 'fa-pen-to-square' : 'fa-file-invoice'"></i>
          {{ isEditing ? 'EDITAR SERVICIO' : 'DETALLE DE SERVICIO' }}
        </h2>
        <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
      </header>

      <!-- VIEW MODE -->
      <div class="service-details-body" v-if="service && !isEditing">
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
            <span class="info-value highlight-green">{{ service.precio !== null ? service.precio + ' €' : 'N/A'
              }}</span>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-subtitle"><i class="fa-solid fa-comment-dots"></i> NOTAS / OBSERVACIONES</h4>
          <div class="notes-box">
            <p v-if="service.nota" class="notes-text">"{{ service.nota }}"</p>
            <p v-else class="notes-text empty-text">Sin notas registradas en esta intervención.</p>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-subtitle"><i class="fa-solid fa-box-open"></i> MATERIALES / REPUESTOS UTILIZADOS</h4>

          <div v-if="service.productos && service.productos.length > 0" class="products-list">
            <div v-for="prod in service.productos" :key="prod.producto_id" class="product-item cell-shaded-inner">
              <div class="product-header">
                <span class="product-brand">{{ prod.marca }}</span>
                <span class="product-qty">x{{ prod.cantidad }}</span>
              </div>
              <div class="product-name">{{ prod.nombre }}</div>
              <div class="product-meta">
                <span v-if="prod.referencia" class="product-ref"><i class="fa-solid fa-hashtag"></i> {{ prod.referencia
                  }}</span>
                <span v-if="prod.categoria" class="product-cat"><i class="fa-solid fa-tags"></i> {{ prod.categoria
                  }}</span>
              </div>
            </div>
          </div>

          <div v-else class="empty-products-box cell-shaded-inner">
            <i class="fa-solid fa-circle-info"></i> No se registraron repuestos o productos en este servicio.
          </div>
        </div>
      </div>

      <!-- EDIT MODE -->
      <form @submit.prevent="saveChanges" class="edit-form-body comic-form" v-else-if="service && isEditing">
        <div class="form-grid">
          <div class="input-group">
            <label class="label-form">Tipo de Servicio:</label>
            <select v-model="editForm.tipo_revision_id" class="input-form select-form" required>
              <option value="" disabled>Selecciona el tipo...</option>
              <option v-for="tipo in tiposRevision" :key="tipo.tipo_revision_id" :value="tipo.tipo_revision_id">
                {{ tipo.nombre }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label class="label-form">Kilometraje:</label>
            <input v-model="editForm.kilometro_servicio" type="number" class="input-form" required min="0">
          </div>

          <div class="input-group">
            <label class="label-form">Fecha:</label>
            <input v-model="editForm.fecha" type="date" class="input-form" required>
          </div>

          <div class="input-group">
            <label class="label-form">Precio Total (€):</label>
            <input v-model="editForm.precio" type="number" step="0.01" class="input-form" min="0">
          </div>

          <div class="input-group" style="grid-column: 1 / -1;">
            <label class="label-form">Notas:</label>
            <textarea v-model="editForm.nota" rows="2" class="input-form"
              placeholder="Ej: Observaciones del mecánico..."></textarea>
          </div>
        </div>

        <!-- Products Section in Edit mode -->
        <div class="products-section cell-shaded-inner">
          <div class="products-header">
            <h4 class="section-subtitle"><i class="fa-solid fa-box-open"></i> PIEZAS / REPUESTOS</h4>
            <button type="button" class="add-product-btn cell-shaded" @click="addProductRow">
              <i class="fa-solid fa-plus"></i> Añadir Pieza
            </button>
          </div>

          <div v-for="(prod, index) in selectedProducts" :key="index" class="product-row">
            <select v-model="prod.producto_id" class="input-form select-form" required>
              <option value="" disabled>Elige un producto...</option>
              <option v-for="item in catalogoProductos" :key="item.producto_id" :value="item.producto_id">
                {{ item.marca }} - {{ item.nombre }}
              </option>
            </select>

            <input v-model="prod.cantidad" type="number" class="input-form qty-input" min="1" required>

            <button type="button" class="delete-row-btn" @click="removeProductRow(index)" title="Quitar pieza">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </div>

          <p v-if="selectedProducts.length === 0" class="no-products-text">
            No se han añadido repuestos a este servicio.
          </p>
        </div>
      </form>

      <!-- ACTIONS -->
      <!-- View mode actions -->
      <div class="modal-actions" v-if="!isEditing">
        <button @click="entrarEditMode" class="btn-edit cell-shaded">
          <i class="fa-solid fa-pen-to-square"></i> EDITAR
        </button>
        <button @click="eliminarServicio" class="btn-delete cell-shaded">
          <i class="fa-solid fa-trash-can"></i> ELIMINAR
        </button>
        <button @click="cerrar" class="btn-close cell-shaded">
          CERRAR
        </button>
      </div>

      <!-- Edit mode actions -->
      <div class="modal-actions" v-else>
        <button @click="saveChanges" class="btn-save cell-shaded">
          <i class="fa-solid fa-floppy-disk"></i> GUARDAR
        </button>
        <button @click="cancelarEdicion" class="btn-cancel cell-shaded">
          CANCELAR
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import api from '@/services/api'
import { useNotificationStore } from '@/stores/notification'

const props = defineProps({
  show: Boolean,
  service: Object
})

const emit = defineEmits(['close', 'updated', 'deleted'])
const notificationStore = useNotificationStore()

const isEditing = ref(false)
const tiposRevision = ref([])
const catalogoProductos = ref([])
const cargandoDropdowns = ref(false)

const editForm = ref({
  tipo_revision_id: '',
  kilometro_servicio: 0,
  precio: null,
  nota: '',
  fecha: ''
})

const selectedProducts = ref([])

const fetchDropdownData = async () => {
  if (tiposRevision.value.length > 0) return
  cargandoDropdowns.value = true
  try {
    const [tiposRes, productosRes] = await Promise.all([
      api.get('/revisiones/tipos/'),
      api.get('/productos/')
    ])
    tiposRevision.value = tiposRes.data
    catalogoProductos.value = productosRes.data
  } catch (error) {
    console.error("Error al cargar catálogos:", error)
  } finally {
    cargandoDropdowns.value = false
  }
}

const entrarEditMode = async () => {
  if (!props.service) return

  editForm.value = {
    tipo_revision_id: props.service.tipo_revision_id,
    kilometro_servicio: props.service.kilometro_servicio,
    precio: props.service.precio,
    nota: props.service.nota || '',
    fecha: props.service.fecha ? props.service.fecha.substring(0, 10) : ''
  }

  selectedProducts.value = (props.service.productos || []).map(p => ({
    producto_id: p.producto_id,
    cantidad: p.cantidad
  }))

  await fetchDropdownData()
  isEditing.value = true
}

const cancelarEdicion = () => {
  isEditing.value = false
}

const addProductRow = () => {
  selectedProducts.value.push({ producto_id: '', cantidad: 1 })
}

const removeProductRow = (index) => {
  selectedProducts.value.splice(index, 1)
}

const saveChanges = async () => {
  try {
    const payload = {
      tipo_revision_id: parseInt(editForm.value.tipo_revision_id),
      kilometro_servicio: parseInt(editForm.value.kilometro_servicio),
      precio: editForm.value.precio !== null && editForm.value.precio !== '' ? parseFloat(editForm.value.precio) : null,
      nota: editForm.value.nota,
      fecha: editForm.value.fecha || null,
      productos_utilizados: selectedProducts.value.map(p => ({
        producto_id: parseInt(p.producto_id),
        cantidad: parseInt(p.cantidad)
      }))
    }

    const response = await api.patch(`/revisiones/${props.service.revision_id}`, payload)

    notificationStore.showSuccess("¡Servicio actualizado con éxito!")
    isEditing.value = false
    emit('updated', response.data)
  } catch (error) {
    console.error("Error al actualizar la revisión:", error)
    notificationStore.showError("Error al guardar los cambios en el servidor.")
  }
}

const eliminarServicio = async () => {
  if (!confirm("¿Seguro que deseas eliminar este servicio de forma permanente? Esta acción no se puede deshacer.")) {
    return
  }

  try {
    await api.delete(`/revisiones/${props.service.revision_id}`)
    notificationStore.showSuccess("¡Servicio eliminado con éxito!")
    emit('deleted', props.service.revision_id)
  } catch (error) {
    console.error("Error al eliminar la revisión:", error)
    notificationStore.showError("Error al intentar eliminar del servidor.")
  }
}

const cerrar = () => {
  isEditing.value = false
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
  transition: border-color 0.3s, box-shadow 0.3s;
}

.modal-content.editing-mode {
  border-color: #ffcc00 !important;
  box-shadow: 12px 12px 0 #000, 0 0 35px rgba(255, 204, 0, 0.2) !important;
}

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

.editing-mode::-webkit-scrollbar-thumb {
  background: #ffcc00;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 3px solid #00ff66;
  padding-bottom: 12px;
  transition: border-color 0.3s;
}

.editing-mode .modal-header {
  border-color: #ffcc00;
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
  transition: color 0.3s;
}

.editing-mode .modal-title {
  color: #ffcc00;
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

.editing-mode .close-btn:hover {
  color: #ffcc00;
}

.service-details-body,
.edit-form-body {
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

  .main-info-grid,
  .secondary-info-grid {
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

/* COMIC FORM STYLING FOR EDIT MODE */
.comic-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

@media (max-width: 480px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-form {
  color: #ffcc00;
  font-family: 'Bangers', cursive;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.input-form {
  background: #000;
  color: #fff;
  border: 2px solid #555;
  padding: 10px 12px;
  font-family: 'Orbitron', sans-serif;
  font-size: 1rem;
  outline: none;
}

.input-form:focus {
  border-color: #ffcc00;
}

.select-form {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

/* Products Section in Edit mode */
.products-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  border: 2px solid #444;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px dashed #444;
  padding-bottom: 8px;
}

.add-product-btn {
  background: #00e5ff;
  color: #000;
  font-family: 'Bangers', cursive;
  font-size: 0.95rem;
  padding: 4px 10px;
  border: 2px solid #000;
  cursor: pointer;
  transition: transform 0.1s;
}

.add-product-btn:hover {
  transform: translate(-1px, -1px);
  box-shadow: 2px 2px 0 #000;
}

.product-row {
  display: grid;
  grid-template-columns: 1fr 70px 40px; 
  gap: 8px;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
}
.qty-input {
  width: 100%; 
  text-align: center;
  box-sizing: border-box;
  padding: 10px 5px !important;
}

.delete-row-btn {
  background: transparent;
  border: none;
  color: #ff3366;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.1s;
}

.delete-row-btn:hover {
  color: #ff00ff;
}

.no-products-text {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
  margin: 5px 0;
  font-style: italic;
}

/* ACTIONS STYLING */
.modal-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.btn-close,
.btn-edit,
.btn-delete,
.btn-save,
.btn-cancel {
  flex: 1;
  min-width: 100px;
  border: 3px solid #000;
  font-family: 'Bangers', cursive;
  padding: 10px 15px;
  font-size: 1.2rem;
  cursor: pointer;
  text-transform: uppercase;
  transition: transform 0.1s, box-shadow 0.1s;
}

.btn-close:hover,
.btn-edit:hover,
.btn-delete:hover,
.btn-save:hover,
.btn-cancel:hover {
  transform: translate(-2px, -2px);
  box-shadow: 3px 3px 0 #000;
}

.btn-close {
  background: #333;
  color: #fff;
}

.btn-edit {
  background: #ffcc00;
  color: #000;
}

.btn-delete {
  background: #ff3366;
  color: #fff;
}

.btn-save {
  background: #00ff66;
  color: #000;
}

.btn-cancel {
  background: #ccc;
  color: #000;
}
</style>
