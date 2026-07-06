<template>
  <Transition name="modal-fade">
    <div class="modal-overlay" @click.self="cerrar">
      <div class="modal-content cell-shaded">
        
        <header class="modal-header">
          <h2 class="modal-title"><i class="fa-solid fa-box-open"></i> REGISTRAR PRODUCTO</h2>
          <button @click="cerrar" class="close-btn"><i class="fa-solid fa-xmark"></i></button>
        </header>
        
        <form @submit.prevent="saveProduct" class="comic-form">
          <div class="form-grid">
            <div class="input-group">
              <label for="marca_prod" class="label-form">Marca:</label>
              <input id="marca_prod" v-model="productForm.marca" type="text" class="input-form" required placeholder="Ej: Castrol">
            </div>

            <div class="input-group">
              <label for="nombre_prod" class="label-form">Nombre:</label>
              <input id="nombre_prod" v-model="productForm.nombre" type="text" class="input-form" required placeholder="Ej: Aceite Sintético 5W-30">
            </div>

            <div class="input-group">
              <label for="referencia_prod" class="label-form">Referencia / Código:</label>
              <input id="referencia_prod" v-model="productForm.referencia" type="text" class="input-form" placeholder="Ej: BR-9902">
            </div>

            <div class="input-group">
              <label for="categoria_prod" class="label-form">Categoría:</label>
              <select id="categoria_prod" v-model="productForm.categoria" class="input-form select-form" required>
                <option value="" disabled>Selecciona una categoría...</option>
                <option value="Aceites y Fluidos">Aceites y Fluidos</option>
                <option value="Filtros">Filtros</option>
                <option value="Frenos">Frenos</option>
                <option value="Motor y Escape">Motor y Escape</option>
                <option value="Suspensión y Dirección">Suspensión y Dirección</option>
                <option value="Baterías y Electricidad">Baterías y Electricidad</option>
                <option value="Neumáticos y Llantas">Neumáticos y Llantas</option>
                <option value="Herramientas y Consumibles">Herramientas y Consumibles</option>
                <option value="Otras Piezas">Otras Piezas</option>
              </select>
            </div>

            <div class="input-group" style="grid-column: 1 / -1;">
              <label for="detalles_prod" class="label-form">Detalles (Opcional):</label>
              <textarea id="detalles_prod" v-model="productForm.detalles" rows="3" class="input-form" placeholder="Especificaciones, cantidad, compatibilidad..."></textarea>
            </div>
          </div>

          <div class="input-group upload-group">
            <label for="imagen_prod" class="label-form">Imagen del Producto:</label>
            <input id="imagen_prod" type="file" @change="handleFileUpload" accept="image/*" class="file-input cell-shaded">
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

const emit = defineEmits(['close', 'refreshProducts'])

const productForm = ref({
  marca: '',
  nombre: '',
  referencia: '',
  categoria: '',
  detalles: '',
  imagen: null
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    productForm.value.imagen = file
  }
}

const cerrar = () => {
  emit('close')
}

const saveProduct = async () => {
  try {
    const formData = new FormData()
    formData.append('marca', productForm.value.marca)
    formData.append('nombre', productForm.value.nombre)
    formData.append('detalles', productForm.value.detalles || '') 
    
    if (productForm.value.referencia) {
      formData.append('referencia', productForm.value.referencia)
    }
    if (productForm.value.categoria) {
      formData.append('categoria', productForm.value.categoria)
    }

    if (productForm.value.imagen) {
      formData.append('archivo_foto', productForm.value.imagen)
    }

    await api.post('/productos/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('refreshProducts')
    cerrar()

  } catch (error) {
    console.error("Error al guardar el producto:", error)
    alert("Hubo un error al guardar el producto. Revisa la consola.")
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
.upload-group { margin-top: 15px; grid-column: 1 / -1; }

.modal-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }
.cancel-btn, .save-btn {
  font-family: 'Bangers', cursive; font-size: 1.2rem; padding: 10px 20px;
  cursor: pointer; transition: transform 0.2s;
}
.cancel-btn { background: #ff3366; color: #fff; border: 3px solid #000; }
.save-btn { background: #ff00ff !important; color: #000 !important; border: 3px solid #000; }
.cancel-btn:hover, .save-btn:hover { transform: translate(-3px, -3px); }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }

/* --- TUS CLASES EXACTAS DE DISEÑO --- */
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

.input-form, .file-input, .select-form {
    padding: 10px 12px !important;
    background: #000 !important;
    color: #ffffff !important;
    border: 2px solid #fff !important;
    outline: none !important;
    transition: border-color 0.2s ease;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Orbitron', sans-serif !important;
}

.input-form:focus, .file-input:focus, .select-form:focus {
    border-color: #00e5ff !important;
}

/* Ajuste específico para que el textarea (Detalles) no se rompa */
textarea.input-form {
    resize: vertical;
    box-sizing: border-box;
    font-family: 'Orbitron', sans-serif !important;
}
</style>