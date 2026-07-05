<template>
  <div class="dashboard-wrapper">
    <header class="section-header cell-shaded">
      <h2 class="section-title">
        <i class="fa-solid fa-box-open"></i> CATÁLOGO DE PRODUCTOS
      </h2>
      
      <button @click="openCreateModal" class="add-btn cell-shaded">
        <i class="fa-solid fa-plus"></i> NUEVO
      </button>
    </header>

    <section class="filters-bar cell-shaded">
      <div class="input-group">
        <i class="fa-solid fa-magnifying-glass search-icon"></i>
        <input 
          type="text" 
          v-model="busquedaNombre" 
          class="brutalist-input search-input" 
          placeholder="Buscar por nombre, marca o referencia..." 
        />
      </div>

      <div class="input-group select-group">
        <select v-model="filtroCategoria" class="brutalist-input select-input">
          <option value="TODOS">TODAS LAS CATEGORÍAS</option>
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
    </section>

    <main class="products-grid">
      <div v-for="prod in productosFiltrados" :key="prod.producto_id" class="product-card cell-shaded">
        
        <div class="product-header">
          <span class="category-badge">{{ prod.categoria || 'Sin categoría' }}</span>
        </div>

        <div class="product-image-container cell-shaded-inner">
          <img 
            v-if="prod.imagen" 
            :src="getImagenUrl(prod.imagen)" 
            alt="Imagen del producto" 
            class="product-image" 
          />
          <div v-else class="no-image-placeholder">
            <i class="fa-solid fa-box-open"></i>
            <span>SIN IMAGEN</span>
          </div>
        </div>

        <h3 class="product-name">{{ prod.nombre }}</h3>
        <p class="product-ref">Ref: {{ prod.referencia || 'N/A' }}</p>

        <div class="product-footer">
          <button @click="abrirModalEdicion(prod)" class="edit-btn cell-shaded" style="width: 100%;">
            <i class="fa-solid fa-pen-to-square"></i> VER / EDITAR
          </button>
        </div>
      </div>

      <div v-if="productosFiltrados.length === 0" class="empty-state cell-shaded">
        <i class="fa-solid fa-ghost"></i>
        <p>No se encontraron productos con esos filtros.</p>
      </div>
    </main>

    <EditProductModal 
      :show="showEditModal" 
      :producto="productoSeleccionado" 
      @close="showEditModal = false" 
      @refresh="fetchProductos" 
    />

    <ProductModal 
      v-if="showCreateModal" 
      @close="showCreateModal = false" 
      @refreshProducts="fetchProductos" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import EditProductModal from '@/components/EditProductModal.vue'
import ProductModal from '@/components/ProductModal.vue'

// --- ESTADO Y VARIABLES ---
const productos = ref([]) // Aquí guardamos TODO lo que viene del backend
const cargando = ref(true)

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const getImagenUrl = (ruta) => {
  if (!ruta) return null
  if (ruta.startsWith('http://') || ruta.startsWith('https://')) {
    return ruta
  }
  return `${baseURL}/media/${ruta}`
}

// Variables para los filtros
const busquedaNombre = ref('')
const filtroCategoria = ref('TODOS')

// Variables para los modales
const showCreateModal = ref(false)
const showEditModal = ref(false)
const productoSeleccionado = ref(null)

// --- OBTENER DATOS DEL BACKEND ---
const fetchProductos = async () => {
  try {
    const response = await api.get('/productos/')
    productos.value = response.data
  } catch (error) {
    console.error("Error cargando el catálogo:", error)
  } finally {
    cargando.value = false
  }
}

onMounted(() => {
  fetchProductos()
})

// --- LA MAGIA DEL FILTRADO (Computed) ---
const productosFiltrados = computed(() => {
  return productos.value.filter(prod => {
    
    // 1. Filtro por texto (busca en nombre, marca o referencia de forma segura)
    const textoBuscado = busquedaNombre.value.toLowerCase()
    const coincideTexto = 
      (prod.nombre && prod.nombre.toLowerCase().includes(textoBuscado)) || 
      (prod.marca && prod.marca.toLowerCase().includes(textoBuscado)) || 
      (prod.referencia && prod.referencia.toLowerCase().includes(textoBuscado))
      
    // 2. Filtro por categoría
    const coincideCategoria = 
      filtroCategoria.value === 'TODOS' || 
      prod.categoria === filtroCategoria.value
      
    return coincideTexto && coincideCategoria
  })
})

// --- FUNCIONES DE BOTONES ---
const openCreateModal = () => {
  showCreateModal.value = true
}

const abrirModalEdicion = (producto) => {
  productoSeleccionado.value = producto
  showEditModal.value = true
}
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* HEADER */
.section-header {
  background: var(--panel-bg, #111);
  padding: 15px 20px;
  margin-bottom: 20px;
  border: 4px solid #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-family: 'Bangers', cursive;
  font-size: 2.5rem;
  color: #00ff66;
  margin: 0;
  letter-spacing: 2px;
}

.add-btn {
  background: #ff00ff;
  color: #fff;
  font-family: 'Bangers', cursive;
  font-size: 1.5rem;
  padding: 8px 20px;
  border: 3px solid #000;
  cursor: pointer;
  transition: transform 0.1s;
}
.add-btn:hover { transform: translate(-3px, -3px); box-shadow: 4px 4px 0 #000; }

/* BARRA DE FILTROS */
.filters-bar {
  background: #1a1a1a;
  padding: 20px;
  border: 4px solid #555;
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.input-group {
  display: flex;
  align-items: center;
  flex: 2;
  position: relative;
}

.select-group {
  flex: 1;
  min-width: 200px;
}

.search-icon {
  position: absolute;
  left: 15px;
  color: #00e5ff;
  font-size: 1.2rem;
}

.search-input {
  width: 100%;
  padding: 12px 15px 12px 45px;
}

.brutalist-input {
  background: #000;
  color: #fff;
  border: 3px solid #00e5ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem;
  outline: none;
}
.brutalist-input:focus { background: #111; border-color: #ffcc00; }

.select-input {
  width: 100%;
  padding: 12px 15px;
  cursor: pointer;
}

/* GRID DE PRODUCTOS */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.product-card {
  background: #111;
  border: 4px solid #fff;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.product-card:hover {
  transform: translateY(-5px);
  border-color: #ffcc00;
  box-shadow: 8px 8px 0px rgba(255, 204, 0, 0.5);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-badge {
  background: #00e5ff;
  color: #000;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.8rem;
  font-weight: bold;
  padding: 4px 8px;
  text-transform: uppercase;
  border: 2px solid #000;
}

/* IMAGE CONTAINER */
.product-image-container {
  height: 160px;
  background: #000;
  border: 3px solid #555;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #666;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  letter-spacing: 1px;
}

.no-image-placeholder i {
  font-size: 2.5rem;
}

.product-name {
  color: #fff;
  font-family: 'Bangers', cursive;
  font-size: 1.8rem;
  margin: 0;
  letter-spacing: 1px;
}

.product-ref {
  color: #aaa;
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
  margin: 0;
}

.product-footer {
  margin-top: auto;
  display: flex;
  justify-content: center;
  border-top: 2px dashed #555;
  padding-top: 15px;
}

.edit-btn {
  background: #fff;
  color: #000;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  padding: 8px 15px;
  border: 3px solid #000;
  cursor: pointer;
  transition: all 0.2s;
}
.edit-btn:hover { background: #00e5ff; }

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 50px;
  border: 4px dashed #555;
  color: #aaa;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.2rem;
}
.empty-state i { font-size: 3rem; margin-bottom: 15px; color: #555; }
</style>