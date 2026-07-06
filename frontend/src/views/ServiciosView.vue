<template>
    <div class="dashboard-wrapper">
        <header class="section-header cell-shaded">
            <h2 class="section-title">
                <i class="fa-solid fa-clock-rotate-left"></i> HISTORIAL DE SERVICIOS
            </h2>

            <button @click="showServiceModal = true" class="add-btn cell-shaded">
                <i class="fa-solid fa-plus"></i> NUEVO SERVICIO
            </button>
        </header>

        <div class="action-bar cell-shaded">
            <div class="input-group search-bar">
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input type="text" v-model="busquedaHistorial" class="brutalist-input search-input"
                    placeholder="Buscar por vehículo o notas..." />
            </div>

            <div class="date-filter-group">
                <div class="date-input-wrapper">
                    <label class="date-label">DESDE:</label>
                    <input type="date" v-model="fechaInicio" class="brutalist-input date-input" />
                </div>
                <div class="date-input-wrapper">
                    <label class="date-label">HASTA:</label>
                    <input type="date" v-model="fechaFin" class="brutalist-input date-input" />
                </div>
                <button @click="limpiarFechas" class="clear-date-btn cell-shaded" title="Limpiar fechas">
                    <i class="fa-solid fa-eraser"></i> LIMPIAR
                </button>
            </div>
        </div>

        <main class="services-grid">
            <div v-for="srv in historialFiltrado" :key="srv.revision_id" class="service-card cell-shaded" @click="verDetalle(srv)">
                <div class="card-header">
                    <span class="type-badge">{{ srv.tipo_revision_nombre || 'Mantenimiento' }}</span>
                    <span class="price-badge">{{ srv.precio }} €</span>
                </div>

                <h3 class="vehicle-title"><i class="fa-solid fa-car"></i> {{ srv.vehiculo_id }}</h3>

                <div class="card-body">
                    <p><i class="fa-solid fa-gauge-high"></i> {{ srv.kilometro_servicio }} km</p>
                    <p class="service-date"><i class="fa-regular fa-calendar"></i> {{ formatearFecha(srv.fecha) }}</p>
                    <p class="notes">"{{ srv.nota || 'Sin notas' }}"</p>
                </div>
            </div>

            <div v-if="historialFiltrado.length === 0" class="empty-state cell-shaded">
                <i class="fa-solid fa-ghost"></i>
                <p>No hay servicios registrados con esos datos.</p>
            </div>
        </main>

        <ServiceModal v-if="showServiceModal" @close="showServiceModal = false" @refreshServices="fetchHistorial" />
        
        <ServiceDetailsModal 
            :show="showDetailsModal" 
            :service="selectedService" 
            @close="showDetailsModal = false" 
            @updated="onServiceUpdated"
            @deleted="onServiceDeleted"
        />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import ServiceModal from '@/components/ServiceModal.vue'
import ServiceDetailsModal from '@/components/ServiceDetailsModal.vue'

const historialServicios = ref([])
const busquedaHistorial = ref('')
const showServiceModal = ref(false)

const showDetailsModal = ref(false)
const selectedService = ref(null)

const verDetalle = (srv) => {
    selectedService.value = srv
    showDetailsModal.value = true
}

const onServiceUpdated = async (updatedSrv) => {
    await fetchHistorial()
    selectedService.value = updatedSrv
}

const onServiceDeleted = async (deletedId) => {
    await fetchHistorial()
    showDetailsModal.value = false
    selectedService.value = null
}

const fechaInicio = ref('')
const fechaFin = ref('')

const fetchHistorial = async () => {
    try {
        const res = await api.get('/revisiones/')
        historialServicios.value = res.data
    } catch (error) {
        console.error("Error al cargar el historial:", error)
    }
}

const limpiarFechas = () => {
    fechaInicio.value = ''
    fechaFin.value = ''
}

const formatearFecha = (fechaStr) => {
    if (!fechaStr) return 'N/A'
    const date = new Date(fechaStr)
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    })
}

onMounted(() => {
    fetchHistorial()
})

const historialFiltrado = computed(() => {
    let filtrado = historialServicios.value

    if (busquedaHistorial.value) {
        const texto = busquedaHistorial.value.toLowerCase()
        filtrado = filtrado.filter(s =>
            (s.nota && s.nota.toLowerCase().includes(texto)) ||
            (s.vehiculo_id && s.vehiculo_id.toLowerCase().includes(texto))
        )
    }

    if (fechaInicio.value) {
        const inicio = new Date(fechaInicio.value)
        inicio.setHours(0, 0, 0, 0)
        filtrado = filtrado.filter(s => {
            const fechaSrv = new Date(s.fecha)
            return fechaSrv >= inicio
        })
    }

    if (fechaFin.value) {
        const fin = new Date(fechaFin.value)
        fin.setHours(23, 59, 59, 999)
        filtrado = filtrado.filter(s => {
            const fechaSrv = new Date(s.fecha)
            return fechaSrv <= fin
        })
    }

    return filtrado
})
</script>

<style scoped>
.dashboard-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.section-header {
    background: var(--panel-bg, #111);
    padding: 15px 20px;
    border: 4px solid #fff;
    margin-bottom: 20px;
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

.add-btn:hover {
    transform: translate(-3px, -3px);
    box-shadow: 4px 4px 0 #000;
}


.action-bar {
    background: #1a1a1a;
    padding: 20px;
    border: 4px solid #555;
    margin-bottom: 30px;
    display: flex;
    gap: 25px;
    flex-wrap: wrap;
    align-items: center;
}

.search-bar {
    position: relative;
    flex: 2;
    min-width: 250px;
}

.search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    color: #00e5ff;
}

.search-input {
    padding-left: 45px !important;
}

.date-filter-group {
    display: flex;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
    flex: 3;
    justify-content: flex-end;
}

.date-input-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
}

.date-label {
    color: #00e5ff;
    font-family: 'Bangers', cursive;
    font-size: 1.2rem;
    letter-spacing: 1px;
}

.date-input {
    padding: 8px 12px !important;
    font-size: 1rem !important;
    cursor: pointer;
}

.clear-date-btn {
    background: #ff3366;
    color: #fff;
    border: 2px solid #000;
    padding: 8px 15px;
    cursor: pointer;
    font-family: 'Bangers', cursive;
    font-size: 1.1rem;
    transition: transform 0.1s;
}
.clear-date-btn:hover {
    transform: translate(-2px, -2px);
    box-shadow: 3px 3px 0 #000;
}

.brutalist-input {
    width: 100%;
    background: #000;
    color: #fff;
    border: 3px solid #00e5ff;
    padding: 12px 15px;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    outline: none;
    box-sizing: border-box;
}

.brutalist-input:focus {
    border-color: #ffcc00;
}


.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 25px;
}

.service-card {
    background: #111;
    border: 3px solid #ff00ff;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.2s;
    cursor: pointer;
}

.service-card:hover {
    transform: translateY(-5px);
    box-shadow: 6px 6px 0px rgba(255, 0, 255, 0.4);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px dashed #555;
    padding-bottom: 10px;
}

.type-badge {
    background: #ff00ff;
    color: #000;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.8rem;
    font-weight: bold;
    padding: 4px 8px;
    text-transform: uppercase;
    border: 2px solid #000;
}

.price-badge {
    color: #00ff66;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3rem;
    font-weight: bold;
}

.vehicle-title {
    color: #00e5ff;
    font-family: 'Bangers', cursive;
    font-size: 1.8rem;
    margin: 0;
}

.card-body {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.service-date {
    font-family: 'Orbitron', sans-serif;
    color: #00e5ff;
    font-size: 0.9rem;
    margin: 0;
}

.notes {
    font-family: 'Roboto', sans-serif;
    color: #aaa;
    font-style: italic;
    font-size: 0.95rem;
    border-left: 3px solid #555;
    padding-left: 10px;
    margin: 0;
}

.empty-state {
    grid-column: 1 / -1;
    text-align: center;
    padding: 50px;
    border: 3px dashed #ff00ff;
    color: #aaa;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.2rem;
}
.empty-state i { font-size: 3rem; margin-bottom: 15px; color: #555; }
</style>