<template>
  <Transition name="modal-fade">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content cell-shaded">
        
        <h2 class="modal-title">
          <i class="fa-solid fa-box-open"></i> REGISTRAR PRODUCTO
        </h2>
        
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

const emit = defineEmits(['close', 'refreshProducts'])

const productForm = ref({
  marca: '',
  nombre: '',
  detalles: '',
  imagen: null
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    productForm.value.imagen = file
  }
}

const saveProduct = async () => {
  try {
    const formData = new FormData()
    formData.append('marca', productForm.value.marca)
    formData.append('nombre', productForm.value.nombre)
    formData.append('detalles', productForm.value.detalles || '') 
    
    if (productForm.value.imagen) {
      formData.append('archivo_imagen', productForm.value.imagen)
    }

    await api.post('/productos/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('refreshProducts')
    emit('close')

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
/* Dejo este botón en amarillo para diferenciarlo del verde de autos, con texto negro para que contraste bien */
.save-btn { background: var(--neon-yellow); color: #000; }
.cancel-btn:hover, .save-btn:hover { transform: translate(-3px, -3px); }
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }

/* --- TUS CLASES EXACTAS DE DISEÑO --- */
.input-group {
    display: grid;
    margin: 0.5em;
}

.label-form {
    margin: 0.35em;
}

.input-form {
    padding: 0.4em;
    background: #111;
    color: #ffffff;
    border: 3px solid #000;
}

/* Ajuste específico para que el textarea (Detalles) no se rompa */
textarea.input-form {
    resize: vertical;
    box-sizing: border-box;
    font-family: 'Roboto', sans-serif;
}
</style>