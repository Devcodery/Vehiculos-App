<template>
  <Transition name="modal-fade">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content cell-shaded">
        
        <h2 class="modal-title">
          <i class="fa-solid fa-wrench"></i> REGISTRAR SERVICIO
        </h2>
        
        <form @submit.prevent="saveService" class="comic-form">
          <div class="form-grid">
            
            <div class="input-group">
              <label for="vehiculo" class="label-form">Vehículo:</label>
              <select id="vehiculo" v-model="serviceForm.vehiculo_id" class="input-form select-form" required>
                <option value="" disabled>Selecciona un coche...</option>
                <option v-for="car in vehiculos" :key="car.matricula" :value="car.matricula">
                  {{ car.matricula }} - {{ car.alias || car.modelo }}
                </option>
              </select>
            </div>

            <div class="input-group">
              <label for="tipo_revision" class="label-form">Tipo de Servicio:</label>
              <select id="tipo_revision" v-model="serviceForm.tipo_revision_id" class="input-form select-form" required>
                <option value="" disabled>Selecciona el tipo...</option>
                <option v-for="tipo in tiposRevision" :key="tipo.tipo_revision_id" :value="tipo.tipo_revision_id">
                  {{ tipo.nombre }}
                </option>
              </select>
            </div>

            <div class="input-group">
              <label for="km_servicio" class="label-form">Kilometraje Actual:</label>
              <input id="km_servicio" v-model="serviceForm.kilometro_servicio" type="number" class="input-form" required min="0" placeholder="Ej: 45000">
            </div>

            <div class="input-group">
              <label for="precio_servicio" class="label-form">Precio Total (€):</label>
              <input id="precio_servicio" v-model="serviceForm.precio" type="number" step="0.01" class="input-form" min="0" placeholder="Ej: 150.50">
            </div>

            <div class="input-group" style="grid-column: 1 / -1;">
              <label for="notas_servicio" class="label-form">Notas:</label>
              <textarea id="notas_servicio" v-model="serviceForm.nota" rows="2" class="input-form" placeholder="Ej: Se observa desgaste en la correa, revisar en la próxima..."></textarea>
            </div>
          </div>

          <div class="products-section cell-shaded-inner">
            <div class="products-header">
              <h3 class="products-title">MATERIALES UTILIZADOS</h3>
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

              <input v-model="prod.cantidad" type="number" class="input-form qty-input" min="1" required placeholder="Cant.">

              <button type="button" class="delete-row-btn" @click="removeProductRow(index)" title="Quitar pieza">
                <i class="fa-solid fa-trash-can"></i>
              </button>
            </div>
            
            <p v-if="selectedProducts.length === 0" class="no-products-text">
              No se han añadido piezas extra a este servicio.
            </p>
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn cell-shaded" @click="$emit('close')">
              CANCELAR
            </button>
            <button type="submit" class="save-btn cell-shaded">
              <i class="fa-solid fa-floppy-disk"></i> REGISTRAR SERVICIO
            </button>
          </div>
        </form>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const emit = defineEmits(['close', 'refreshServices'])

// --- ESTADOS PARA LOS DESPLEGABLES ---
const vehiculos = ref([])
const tiposRevision = ref([])
const catalogoProductos = ref([])

// --- ESTADO DEL FORMULARIO PRINCIPAL ---
const serviceForm = ref({
  vehiculo_id: '',
  tipo_revision_id: '',
  kilometro_servicio: 0,
  precio: null,
  nota: ''
})

// --- ESTADO DINÁMICO DE PRODUCTOS ---
const selectedProducts = ref([])

// Función para cargar datos al abrir el modal
const fetchDropdownData = async () => {
  try {
    // Usamos Promise.all para hacer las 3 peticiones a la vez (más rápido)
    // ⚠️ Asegúrate de tener endpoints GET para estas rutas en main.py
    const [vehiculosRes, tiposRes, productosRes] = await Promise.all([
      api.get('/mis-vehiculos/'),
      api.get('/mis-tipos-revisiones/'), 
      api.get('/productos/')
    ])
    
    vehiculos.value = vehiculosRes.data
    tiposRevision.value = tiposRes.data
    catalogoProductos.value = productosRes.data
  } catch (error) {
    console.error("Error cargando catálogos:", error)
  }
}

// Funciones para manejar las filas de productos
const addProductRow = () => {
  selectedProducts.value.push({ producto_id: '', cantidad: 1 })
}

const removeProductRow = (index) => {
  selectedProducts.value.splice(index, 1)
}

// Ejecutar la carga de datos al montar el componente
onMounted(() => {
  fetchDropdownData()
})

// Enviar datos a FastAPI
const saveService = async () => {
  try {
    // Construimos el DTO exacto (RevisionCreateIn)
    const payload = {
      vehiculo_id: serviceForm.value.vehiculo_id,
      tipo_revision_id: parseInt(serviceForm.value.tipo_revision_id),
      kilometro_servicio: serviceForm.value.kilometro_servicio,
      precio: serviceForm.value.precio || 0,
      nota: serviceForm.value.nota || "",
      // Mapeamos el array para asegurar que los tipos sean correctos
      productos_utilizados: selectedProducts.value.map(p => ({
        producto_id: parseInt(p.producto_id),
        cantidad: parseInt(p.cantidad)
      }))
    }

    await api.post('/revisiones/', payload)
    
    emit('refreshServices')
    emit('close')

  } catch (error) {
    console.error("Error al registrar servicio:", error)
    alert("Hubo un error al registrar el servicio. Revisa la consola.")
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
  background: var(--panel-bg); padding: 30px; width: 90%; max-width: 600px;
  border: 5px solid var(--neon-pink); box-shadow: 12px 12px 0 #000, 0 0 30px rgba(255, 0, 255, 0.3);
  max-height: 95vh; overflow-y: auto; /* Por si añaden muchos productos, que haga scroll */
}
.modal-title {
  font-family: 'Orbitron', sans-serif; color: var(--neon-pink); font-size: 1.8rem;
  margin-top: 0; margin-bottom: 25px; text-align: center;
  -webkit-text-stroke: 1px #000; text-shadow: 2px 2px 0 #000;
}

/* Rejilla principal */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; } 

/* --- ZONA DE PRODUCTOS --- */
.products-section {
  background: #1a1a1a;
  border: 3px dashed #444;
  padding: 15px;
  margin-top: 10px;
}
.products-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
}
.products-title {
  color: #fff; font-family: 'Orbitron', sans-serif; font-size: 1.1rem; margin: 0;
}
.add-product-btn {
  background: #9d00ff; color: #fff; border: 2px solid #000; font-family: 'Bangers', cursive;
  padding: 5px 15px; cursor: pointer; transition: transform 0.2s; font-size: 1rem;
}
.add-product-btn:hover { transform: translate(-2px, -2px); box-shadow: 3px 3px 0 #000; }

.product-row {
  display: grid; grid-template-columns: 1fr 80px 40px; gap: 10px; margin-bottom: 10px; align-items: center;
}
.qty-input { text-align: center; }
.delete-row-btn {
  background: #ff3366; color: #fff; border: 2px solid #000; padding: 8px; cursor: pointer;
  transition: transform 0.2s;
}
.delete-row-btn:hover { transform: scale(1.1); }
.no-products-text {
  text-align: center; color: #666; font-style: italic; margin: 10px 0 0 0; font-size: 0.9rem;
}

/* --- BOTONES INFERIORES --- */
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }
.cancel-btn, .save-btn {
  font-family: 'Bangers', cursive; font-size: 1.2rem; padding: 10px 20px;
  cursor: pointer; transition: transform 0.2s;
}
.cancel-btn { background: #ff3366; color: #fff; }
.save-btn { background: var(--neon-pink); color: #000; }
.cancel-btn:hover, .save-btn:hover { transform: translate(-3px, -3px); }

/* --- TU DISEÑO DE CLASES --- */
.input-group { display: grid; margin: 0.5em; }
.label-form { margin: 0.35em; color: #eee; }
.input-form {
    padding: 0.4em;
    background: #111;
    color: #ffffff;
    border: 3px solid #000;
}
textarea.input-form { resize: vertical; box-sizing: border-box; font-family: 'Roboto', sans-serif; }
.select-form { cursor: pointer; }

/* --- LIMPIADOR DE FLECHAS --- */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
input[type="number"] { -moz-appearance: textfield; appearance: textfield; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }
</style>