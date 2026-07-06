<template>
  <div class="dashboard-wrapper">

    <main class="main-content">
      <div class="welcome-banner cell-shaded">
        <h2>Bienvenido, <span class="highlight">{{ authStore.user?.nombre || 'Piloto' }}</span></h2>
      </div>

      <div class="two-columns">

        <section class="column cars-column">
          <h3 class="column-title">Mi Garaje</h3>

          <div class="cars-list">

            <div v-for="car in cars" :key="car.matricula" class="car-card cell-shaded">
              <div class="car-info">
                <h4>
                  {{ car.marca }} {{ car.modelo }}
                  <span v-if="car.alias">/ {{ car.alias }}</span>
                </h4>
                <p>Matrícula: <strong>{{ car.matricula }}</strong></p>
              </div>

              <div class="km-section cell-shaded-inner">
                <div class="km-display">
                  <i class="fa-solid fa-gauge-high"></i>
                  <span class="km-number">{{ car.kilometraje }}</span> km
                </div>

                <button @click="abrirModalKilometraje(car)" class="btn-update-km cell-shaded">
                  <i class="fa-solid fa-pen"></i> Actualizar
                </button>
              </div>

              <button @click="verVehiculo(car.matricula)" class="view-btn cell-shaded">Ver</button>
            </div>

            <div v-if="cars.length === 0" class="car-card cell-shaded" style="justify-content: center; color: #aaa;">
              <p>Tu garaje está vacío. ¡Añade tu primer auto!</p>
            </div>

          </div>
        </section>

        <section class="column actions-column">
          <h3 class="column-title">Opciones</h3>

          <div class="action-grid">

            <button class="tile-btn cell-shaded" @click="openCarModal">
              <i class="fa-solid fa-car tile-icon"></i>
              <h3 class="tile-title">AGREGAR AUTO</h3>
              <p class="tile-desc">Registro de nueva unidad al garaje.</p>
            </button>

            <button class="tile-btn cell-shaded" @click="openProductModal">
              <i class="fa-solid fa-box-open tile-icon"></i>
              <h3 class="tile-title">AGREGAR PRODUCTO</h3>
              <p class="tile-desc">Gestión de inventario de repuestos y consumibles.</p>
            </button>

            <button class="tile-btn cell-shaded" @click="openServiceModal">
              <i class="fa-solid fa-wrench tile-icon"></i>
              <h3 class="tile-title">AGREGAR SERVICIO</h3>
              <p class="tile-desc">Creación de órdenes de trabajo y mantenimientos.</p>
            </button>

            <button class="tile-btn cell-shaded" @click="openServiceTypeModal">
              <i class="fa-solid fa-clipboard-check tile-icon"></i>
              <h3 class="tile-title">AGREGAR TIPO SERVICIO</h3>
              <p class="tile-desc">Configuración de protocolos de mantenimiento.</p>
            </button>

          </div>
        </section>

      </div>
    </main>

    <CarModal v-if="showCarModal" @close="showCarModal = false" @refresh-garage="fetchVehiculos">
    </CarModal>

    <ProductModal v-if="showProductoModal" @close="showProductoModal = false">
    </ProductModal>

    <ServiceTypeModal v-if="showServiceTypeModal" @close="showServiceTypeModal = false">
    </ServiceTypeModal>

    <ServiceModal v-if="showServiceModal" @close="showServiceModal = false">
    </ServiceModal>

    <UpdateKmModal 
      :show="showKmModal" 
      :car="cocheSeleccionadoParaKm"
      @close="showKmModal = false"
      @save="procesarNuevoKm"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import CarModal from '@/components/CarModal.vue'
import ProductModal from '@/components/ProductModal.vue'
import ServiceTypeModal from '@/components/ServiceTypeModal.vue'
import ServiceModal from '@/components/ServiceModal.vue'
import UpdateKmModal from '@/components/UpdateKmModal.vue'

const authStore = useAuthStore()
const router = useRouter()

const cars = ref([])
const showCarModal = ref(false)
const showProductoModal = ref(false)
const showServiceTypeModal = ref(false)
const showServiceModal = ref(false)
const showKmModal = ref(false)
const cocheSeleccionadoParaKm = ref(null)


const fetchVehiculos = async () => {
  try {
    const response = await api.get('/vehiculos/')

    cars.value = response.data
  } catch (error) {
    console.error('Error al cargar el garaje:', error)
  }
}

const enviarParcheVehiculo = async (idIdentificador, datosCambiados) => {
  try {
    const response = await api.patch(`/vehiculos/${idIdentificador}`, datosCambiados)
    return { success: true, data: response.data }
  } catch (error) {
    console.error("Error al actualizar el vehículo:", error)
    alert("Error de comunicación con el servidor.")
    return { success: false }
  }
}

const abrirModalKilometraje = (car) => {
  cocheSeleccionadoParaKm.value = car
  showKmModal.value = true
}

const procesarNuevoKm = async (nuevoKmValor) => {
  const coche = cocheSeleccionadoParaKm.value
  const idCoche = coche.id || coche.matricula 
  
  const resultado = await enviarParcheVehiculo(idCoche, { kilometraje: nuevoKmValor })

  if (resultado.success) {
    coche.kilometraje = nuevoKmValor
    showKmModal.value = false
  } else {
    alert("Error al guardar en la base de datos.")
  }
}

const verVehiculo = (matricula) => {
  router.push(`/vehiculo/${matricula}`)
}

onMounted(() => {
  fetchVehiculos()
})


const openCarModal = () => {
  showCarModal.value = true
}

const openProductModal = () => {
  showProductoModal.value = true
}

const openServiceTypeModal = () => {
  showServiceTypeModal.value = true
}

const openServiceModal = () => {
  showServiceModal.value = true
}

const verDetallesVehiculo = (matricula) => {
  router.push({ name: 'VehiculoDetalle', params: { id: matricula } })
}
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}



.welcome-banner {
  background: rgba(0, 0, 0, 0.8);
  padding: 20px 30px;
  margin-bottom: 30px;
  border-color: var(--neon-yellow);
}

.welcome-banner h2 {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.8rem;
  margin: 0;
  color: #fff;
}

.welcome-banner .highlight {
  color: var(--neon-yellow);
  text-transform: uppercase;
  -webkit-text-stroke: 1px #000;
  text-shadow: 2px 2px 0 #000;
}


.two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

@media (max-width: 900px) {
  .two-columns {
    grid-template-columns: 1fr;
  }
}

.column-title {
  font-family: 'Bangers', cursive;
  font-size: 2.2rem;
  color: #fff;
  margin-bottom: 20px;
  letter-spacing: 1px;
  text-shadow: 2px 2px 0 #000;
}


.cars-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.car-card {
  display: flex;
  flex-direction: column; 
  gap: 15px; 
  padding: 20px;
  
}

.car-card:hover {
  transform: translateX(5px);
  border-color: var(--neon-blue);
}

.car-info h4 {
  font-family: 'Orbitron', sans-serif;
  margin: 0 0 5px 0;
  font-size: 1.4rem;
  color: #00e5ff;
  text-shadow: 1px 1px 0px #000;
}

.car-info p {
  margin: 0;
  color: #ccc;
  font-size: 0.9rem;
}

.view-btn {
  width: 100%;
  margin-top: auto; 
  padding: 10px;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  text-transform: uppercase;
  
}

.view-btn:hover {
  background: var(--neon-blue);
  color: #000;
}




.action-grid {
  display: grid;
  
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.tile-btn {
  background: #1c1f2b;
  
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.tile-btn:hover {
  transform: translate(-5px, -5px);
  box-shadow: 11px 11px 0 #000, 0 0 20px rgba(255, 0, 255, 0.4);
}

.tile-icon {
  font-size: 50px;
  
  color: var(--neon-pink);
  margin-bottom: 20px;
  filter: drop-shadow(2px 2px 0px #000);
}

.tile-title {
  color: var(--neon-yellow);
  
  font-family: 'Bangers', cursive;
  font-size: 1.6rem;
  margin: 0 0 15px 0;
  letter-spacing: 1.5px;
  -webkit-text-stroke: 1px #000;
  text-shadow: 2px 2px 0px #000;
}

.tile-desc {
  color: #dae1e7;
  
  font-family: 'Roboto', sans-serif;
  font-size: 0.95rem;
  margin: 0;
  line-height: 1.4;
}

.menu-icon {
  font-size: 35px;
  
}

.km-section {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  flex-wrap: wrap; 
  gap: 10px;
  
  background: rgba(0, 0, 0, 0.4);
  border: 2px dashed #555; 
  padding: 12px 15px;
}

.km-display {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #00e5ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem;
}

.km-number {
  font-size: 1.8rem;
  font-weight: bold;
  letter-spacing: 2px; 
}

.btn-update-km {
  background: #ffcc00;
  color: #000;
  border: 3px solid #000;
  font-family: 'Bangers', cursive;
  padding: 6px 12px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.1s;
  box-shadow: 3px 3px 0 #000;
}

.btn-update-km:hover {
  transform: translate(-2px, -2px);
  box-shadow: 5px 5px 0 #000;
}
</style>