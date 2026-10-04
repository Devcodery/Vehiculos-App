<template>
  <div v-if="show" class="modal-overlay" @click="cerrar"></div>

  <div v-if="show" class="brutalist-modal cell-shaded">
    <header class="modal-header">
      <h2 class="modal-title"><i class="fa-solid fa-pen-to-square"></i> VER / EDITAR PRODUCTO</h2>
      <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
    </header>

    <main class="modal-body">
      <form @submit.prevent="guardarCambios" class="modal-form">
        
        <div class="two-fields">
          <div class="input-group">
            <label>NOMBRE DEL PRODUCTO</label>
            <input type="text" v-model="formulario.nombre" class="brutalist-input" required placeholder="Ej: Pastillas de freno" />
          </div>

          <div class="input-group">
            <label>MARCA</label>
            <input type="text" v-model="formulario.marca" class="brutalist-input" required placeholder="Ej: Brembo" />
          </div>
        </div>

        <div class="two-fields">
          <div class="input-group">
            <label>REFERENCIA / CÓDIGO</label>
            <input type="text" v-model="formulario.referencia" class="brutalist-input" placeholder="Ej: BR-9902" />
          </div>

          <div class="input-group">
            <label>CATEGORÍA</label>
            <select v-model="formulario.categoria" class="brutalist-input brutalist-select" required>
              <option value="Aceites y Fluidos">Aceites y Fluidos</option>
              <option value="Filtros">Filtros</option>
              <option value="Discos y Frenos">Discos y Frenos</option>
              <option value="Motor y Escape">Motor y Escape</option>
              <option value="Suspensión y Dirección">Suspensión y Dirección</option>
              <option value="Baterías y Electricidad">Baterías y Electricidad</option>
              <option value="Neumáticos y Llantas">Neumáticos y Llantas</option>
              <option value="Herramientas y Consumibles">Herramientas y Consumibles</option>
              <option value="Otras Piezas">Otras Piezas</option>
            </select>
          </div>
        </div>

        <div class="input-group">
          <label>TIPO DE SERVICIO ASOCIADO</label>
          <select v-model="formulario.tipo_revision_id" class="brutalist-input brutalist-select">
            <option :value="null">Cualquiera / General</option>
            <option v-for="tipo in tiposRevision" :key="tipo.tipo_revision_id" :value="tipo.tipo_revision_id">
              {{ tipo.nombre }}
            </option>
          </select>
        </div>

        <div class="input-group">
          <label>IMAGEN DEL PRODUCTO</label>
          <div class="image-preview-container cell-shaded-inner">
            <img 
              v-if="imagenUrl" 
              :src="imagenUrl" 
              alt="Imagen del producto" 
              class="modal-product-img" 
            />
            <div v-else class="no-img-placeholder">
              <i class="fa-solid fa-box-open"></i>
              <span>SIN IMAGEN ASIGNADA</span>
            </div>
          </div>
        </div>

        <div class="input-group upload-group">
          <label class="label-form">Cambiar Imagen:</label>
          <input type="file" @change="handleFileUpload" accept="image/*" class="file-input cell-shaded" />
        </div>

        <div class="input-group">
          <label>DETALLES TÉCNICOS</label>
          <textarea v-model="formulario.detalles" class="brutalist-input brutalist-textarea" rows="3" placeholder="Especificaciones adicionales..."></textarea>
        </div>

        <div v-if="mensaje" :class="['mensaje-alerta', tipoMensaje]">
          {{ mensaje }}
        </div>

        <div class="form-actions">
          <button type="submit" class="save-btn cell-shaded" :disabled="cargando">
            <i class="fa-solid fa-floppy-disk"></i> {{ cargando ? 'GUARDANDO...' : 'GUARDAR' }}
          </button>
          
          <button type="button" @click="eliminarProducto" class="delete-btn cell-shaded" :disabled="cargando">
            <i class="fa-solid fa-trash-can"></i> ELIMINAR
          </button>
        </div>

      </form>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import api from '@/services/api'

const props = defineProps({
  show: Boolean,
  producto: Object
})

const emit = defineEmits(['close', 'refresh'])

const tiposRevision = ref([])

const formulario = ref({
  nombre: '',
  marca: '',
  referencia: '',
  categoria: '',
  tipo_revision_id: null,
  imagen: '',
  detalles: ''
})

const archivoImagen = ref(null)
const previewImagen = ref(null)
const cargando = ref(false)
const mensaje = ref('')
const tipoMensaje = ref('')

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const imagenUrl = computed(() => {
  if (previewImagen.value) {
    return previewImagen.value
  }
  if (!formulario.value.imagen) return null
  if (formulario.value.imagen.startsWith('http://') || formulario.value.imagen.startsWith('https://')) {
    return formulario.value.imagen
  }
  return `${baseURL}/media/${formulario.value.imagen}`
})

const fetchTipos = async () => {
  try {
    const res = await api.get('/revisiones/tipos/')
    tiposRevision.value = res.data
  } catch (error) {
    console.error("Error cargando tipos de revisión:", error)
  }
}

onMounted(() => {
  fetchTipos()
})

watch(() => props.producto, (nuevoProducto) => {
  if (nuevoProducto) {
    formulario.value = {
      ...nuevoProducto,
      tipo_revision_id: nuevoProducto.tipo_revision_id ?? null
    }
    archivoImagen.value = null
    previewImagen.value = null
  }
}, { immediate: true })

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    archivoImagen.value = file
    previewImagen.value = URL.createObjectURL(file)
  }
}

const cerrar = () => {
  mensaje.value = ''
  archivoImagen.value = null
  previewImagen.value = null
  emit('close')
}

const guardarCambios = async () => {
  cargando.value = true
  mensaje.value = ''
  try {
    const formData = new FormData()
    formData.append('marca', formulario.value.marca)
    formData.append('nombre', formulario.value.nombre)
    formData.append('detalles', formulario.value.detalles || '')
    
    if (formulario.value.referencia) {
      formData.append('referencia', formulario.value.referencia)
    }
    if (formulario.value.categoria) {
      formData.append('categoria', formulario.value.categoria)
    }
    formData.append('tipo_revision_id', formulario.value.tipo_revision_id ? formulario.value.tipo_revision_id : '')

    if (archivoImagen.value) {
      formData.append('archivo_foto', archivoImagen.value)
    }

    await api.patch(`/productos/${props.producto.producto_id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    mensaje.value = '¡Producto actualizado correctamente!'
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

const eliminarProducto = async () => {
  if (!confirm(`¿Seguro que deseas eliminar "${props.producto.nombre}" por completo?`)) return
  cargando.value = true
  try {
    await api.delete(`/productos/${props.producto.producto_id}`)
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
  max-height: 90vh;
  overflow-y: auto;
  background: #111 !important;
  border: 4px solid #ff00ff !important;
  box-shadow: 12px 12px 0 #000, 0 0 30px rgba(255, 0, 255, 0.3) !important;
  z-index: 1101;
  display: flex;
  flex-direction: column;
}

.image-preview-container {
  height: 180px;
  background: #000;
  border: 2px solid #555;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
  box-sizing: border-box;
}

.modal-product-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #080808;
}

.no-img-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #666;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
}

.no-img-placeholder i {
  font-size: 2.2rem;
  color: #444;
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

.upload-group {
  grid-column: 1 / -1;
}

.two-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

label, .input-group label, .label-form {
  color: #00e5ff !important;
  font-family: 'Bangers', cursive !important;
  font-size: 1.2rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
}

.brutalist-input, .file-input {
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
.brutalist-input:focus, .file-input:focus { border-color: #00e5ff !important; }
.brutalist-select { cursor: pointer; }
.file-input { cursor: pointer; }

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