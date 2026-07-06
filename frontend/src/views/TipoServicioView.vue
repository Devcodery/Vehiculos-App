<template>
    <div class="dashboard-wrapper">
        <header class="section-header cell-shaded">
            <h2 class="section-title">
                <i class="fa-solid fa-clipboard-list"></i> TIPOS DE SERVICIO
            </h2>

            <button @click="showServiceTypeModal = true" class="add-btn cell-shaded">
                <i class="fa-solid fa-plus"></i> NUEVO TIPO
            </button>
        </header>

        <main class="services-grid">
            <div v-for="tipo in tiposServicio" :key="tipo.tipo_revision_id" class="type-card cell-shaded">
                <h3 class="type-title">{{ tipo.nombre }}</h3>

                <div class="type-details">
                    <div class="detail-box">
                        <i class="fa-solid fa-road"></i>
                        <span>Cada {{ tipo.cada_cuantos_Km }} km</span>
                    </div>
                    <div class="detail-box">
                        <i class="fa-regular fa-calendar"></i>
                        <span>Cada {{ tipo.cada_cuantos_Meses }} meses</span>
                    </div>
                </div>

                <p class="type-desc">{{ tipo.detalles || 'Sin detalles adicionales.' }}</p>

                <div class="type-footer" style="margin-top: auto; border-top: 2px dashed #555; padding-top: 15px;">
                    <button @click="abrirModalEdicion(tipo)" class="edit-btn cell-shaded" style="width: 100%;">
                        <i class="fa-solid fa-pen-to-square"></i> VER / EDITAR
                    </button>
                </div>
            </div>

            <div v-if="tiposServicio.length === 0" class="empty-state cell-shaded">
                <p>No hay tipos de servicio en el catálogo.</p>
            </div>
        </main>

        <ServiceTypeModal v-if="showServiceTypeModal" @close="showServiceTypeModal = false"
            @refreshServices="fetchTipos" />

        <EditServiceTypeModal 
            :show="showEditModal" 
            :tipoServicio="tipoSeleccionado" 
            @close="showEditModal = false" 
            @refresh="fetchTipos" 
        />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import ServiceTypeModal from '@/components/ServiceTypeModal.vue'
import EditServiceTypeModal from '@/components/EditServiceTypeModal.vue'

const tiposServicio = ref([])
const showServiceTypeModal = ref(false)
const showEditModal = ref(false)
const tipoSeleccionado = ref(null)

const fetchTipos = async () => {
    try {
        const res = await api.get('/revisiones/tipos/')
        tiposServicio.value = res.data
    } catch (error) {
        console.error("Error al cargar los tipos:", error)
    }
}

const abrirModalEdicion = (tipo) => {
    tipoSeleccionado.value = tipo
    showEditModal.value = true
}

onMounted(() => {
    fetchTipos()
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
    margin-bottom: 30px;
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

.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 25px;
}

.type-card {
    background: #111;
    border: 3px solid #ff00ff;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.2s;
}

.type-card:hover {
    transform: translateY(-5px);
    box-shadow: 6px 6px 0px rgba(255, 0, 255, 0.4);
}

.type-title {
    color: #00e5ff;
    font-family: 'Bangers', cursive;
    font-size: 1.8rem;
    margin: 0;
}

.type-desc {
    font-family: 'Roboto', sans-serif;
    color: #aaa;
    font-style: italic;
    font-size: 0.95rem;
    border-left: 3px solid #555;
    padding-left: 10px;
    margin: 0;
}

.type-details {
    display: flex;
    gap: 15px;
}

.detail-box {
    background: #000;
    border: 2px solid #555;
    padding: 10px;
    flex: 1;
    text-align: center;
    color: #fff;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.9rem;
}

.detail-box i {
    color: #00e5ff;
    display: block;
    font-size: 1.5rem;
    margin-bottom: 5px;
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
    padding: 40px;
    border: 3px dashed #ff00ff;
    color: #aaa;
    font-family: 'Orbitron', sans-serif;
}
</style>