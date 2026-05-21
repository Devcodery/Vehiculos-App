<template>
  <div class="dashboard-wrapper">

    <header class="top-nav cell-shaded">
     <div class="nav-left">
        <button class="hamburger-btn">
          <i class="fa-solid fa-bars menu-icon"></i>
        </button>
      </div>
      <div class="nav-center">
        <h1 class="brand-title">AutoCare</h1>
      </div>
      <div class="nav-right">
        <button @click="handleLogout" class="logout-btn cell-shaded">
          SALIR <i class="fa-solid fa-power-off"></i>
        </button>
      </div>
    </header>

    <main class="main-content">
      <div class="welcome-banner cell-shaded">
        <h2>Bienvenido, <span class="highlight">{{ authStore.user?.nombre || 'Piloto' }}</span></h2>
      </div>

      <div class="two-columns">

        <section class="column cars-column">
          <h3 class="column-title">Mi Garaje</h3>

          <div class="cars-list">
            
            <div 
              v-for="car in cars" 
              :key="car.matricula" 
              class="car-card cell-shaded"
            >
              <div class="car-info">
                <h4>
                  {{ car.marca }} {{ car.modelo }} 
                  <span v-if="car.alias">/ {{ car.alias }}</span>
                </h4>
                <p>Matrícula: <strong>{{ car.matricula }}</strong></p>
              </div>
              <button class="view-btn cell-shaded">Ver</button>
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

            <button class="tile-btn cell-shaded" @click="goTo('add-product')">
              <i class="fa-solid fa-box-open tile-icon"></i>
              <h3 class="tile-title">AGREGAR PRODUCTO</h3>
              <p class="tile-desc">Gestión de inventario de repuestos y consumibles.</p>
            </button>

            <button class="tile-btn cell-shaded" @click="goTo('add-service')">
              <i class="fa-solid fa-wrench tile-icon"></i>
              <h3 class="tile-title">AGREGAR SERVICIO</h3>
              <p class="tile-desc">Creación de órdenes de trabajo y mantenimientos.</p>
            </button>

            <button class="tile-btn cell-shaded" @click="goTo('add-revision')">
              <i class="fa-solid fa-clipboard-check tile-icon"></i>
              <h3 class="tile-title">TIPO REVISIÓN</h3>
              <p class="tile-desc">Configuración de protocolos de mantenimiento.</p>
            </button>

          </div>
        </section>

      </div>
    </main>

    <Transition name="modal-fade">
     <div v-if="showCarModal" class="modal-overlay" @click.self="closeCarModal">
        <div class="modal-content cell-shaded">
          
          <h2 class="modal-title">
            <i class="fa-solid fa-car"></i> REGISTRAR AUTO
          </h2>
          
          <form @submit.prevent="saveCar" class="comic-form">
            <div class="form-grid">
              <div class="input-group">
                <label>Marca:</label>
                <input v-model="carForm.marca" type="text" required placeholder="Ej: Nissan">
              </div>

              <div class="input-group">
                <label>Modelo:</label>
                <input v-model="carForm.modelo" type="text" required placeholder="Ej: Skyline R34">
              </div>

              <div class="input-group">
                <label>Matrícula:</label>
                <input v-model="carForm.matricula" type="text" required placeholder="Ej: GTR-001">
              </div>

              <div class="input-group">
                <label>Kilometraje:</label>
                <input v-model="carForm.kilometraje" type="number" required min="0" placeholder="Ej: 15000">
              </div>

              <div class="input-group">
                <label>Alias :</label>
                <input v-model="carForm.alias" type="text" placeholder="Ej: Godzilla">
              </div>
            </div>

            <div class="input-group upload-group">
              <label>Foto del Vehículo:</label>
              <input type="file" @change="handleFileUpload" accept="image/*" class="file-input cell-shaded">
            </div>

            <div class="modal-actions">
              <button type="button" class="cancel-btn cell-shaded" @click="closeCarModal">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const authStore = useAuthStore()
const router = useRouter()

const cars = ref([])
const showCarModal = ref(false)
const carForm = ref({
  marca: '',
  modelo: '',
  matricula: '',
  alias: '',
  kilometraje: 0,
  foto: null
})

// Funcion para extraer los vehiculos del usuario de la base de datos
const fetchVehiculos = async () => {
  try {
    // Peticion a la ruta
    const response = await api.get('/mis-vehiculos/')

    cars.value = response.data


  }catch(error){
    console.error('Error al cargar el garaje:', error)
  }
}

// Con esto hacemos que se cargue nada abrir la pagina
onMounted(() => {
  fetchVehiculos()
})

// --- LÓGICA DEL MODAL DE VEHÍCULOS ---

// Abrir el registrar carro
const openCarModal = () => {
  showCarModal.value = true
}

// Cerrar el registrar carro
const closeCarModal = () => {
  showCarModal.value = false

  //Limpiamos el formulario
  carForm.value = { marca: '', modelo: '', matricula: '', alias: '', foto: null }
}

// Controlamos el subir una imagen
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    carForm.value.foto = file
  }
}

const saveCar = async () => {
  try {
    // Al llevar imagen, DEBEMOS usar FormData
    const formData = new FormData()
    formData.append('marca', carForm.value.marca)
    formData.append('modelo', carForm.value.modelo)
    formData.append('matricula', carForm.value.matricula)
    formData.append('kilometraje', carForm.value.kilometraje)
    formData.append('alias', carForm.value.alias || "")
    
    // Si el usuario subió una foto, la metemos en el paquete
    if (carForm.value.foto) {
      formData.append('foto', carForm.value.foto)
    }

    // Hacemos el POST (Asegúrate de que la ruta coincida con tu backend)
    await api.post('/vehiculos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Si sale bien, cerramos el modal y recargamos el garaje
    closeCarModal()
    fetchVehiculos() 

  } catch (error) {
    console.error("Error al guardar el coche:", error)
    alert("Hubo un error al guardar el vehículo. Revisa la consola.")
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const goTo = (routeName) => {
  console.log(`Navegando a: ${routeName}`)
  router.push({ name: routeName })
}
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* --- HEADER --- */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--panel-bg);
  padding: 15px 30px;
  margin-bottom: 30px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.brand-title {
  font-family: 'Orbitron', sans-serif;
  font-style: italic;
  font-size: 3rem;
  color: var(--neon-blue);
  margin: 0;
  -webkit-text-stroke: 1.5px #000;
  text-shadow: 3px 3px 0 #000;
}

.hamburger-btn {
  background: none;
  border: none;
  color: #00ff66;
  cursor: pointer;
  padding: 5px;
  transition: transform 0.2s;
}

.hamburger-btn:hover {
  transform: scale(1.1);
}

.icon-svg {
  width: 35px;
  height: 35px;
}

.logout-btn {
  background: var(--neon-pink);
  color: #000;
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  padding: 8px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: transform 0.2s;
}

.logout-btn:hover {
  transform: translate(-3px, -3px);
  box-shadow: 9px 9px 0 #000, 0 0 15px rgba(255, 0, 255, 0.6);
}

/* --- WELCOME BANNER --- */
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

/* --- GRID DE 2 COLUMNAS --- */
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

/* --- TARJETAS DE COCHES --- */
.cars-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.car-card {
  background: var(--panel-bg);
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s;
}

.car-card:hover {
  transform: translateX(5px);
  border-color: var(--neon-blue);
}

.car-info h4 {
  font-family: 'Orbitron', sans-serif;
  color: var(--neon-blue);
  margin: 0 0 5px 0;
  font-size: 1.2rem;
  text-shadow: 1px 1px 0 #000;
}

.car-info p {
  margin: 0;
  color: #ccc;
  font-size: 0.9rem;
}

.view-btn {
  background: var(--dark-bg);
  color: #fff;
  font-family: 'Roboto', sans-serif;
  font-weight: bold;
  padding: 8px 15px;
  cursor: pointer;
  transition: background 0.2s;
}

.view-btn:hover {
  background: var(--neon-blue);
  color: #000;
}

/* ================================================= */
/* 🎨 BOTONES TIPO "TILE" (INSPIRADOS EN LA IMAGEN)  */
/* ================================================= */
.action-grid {
  display: grid;
  /* Esto hace que los botones se coloquen uno al lado del otro si hay espacio */
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.tile-btn {
  background: #1c1f2b;
  /* Fondo azul oscuro/morado */
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
  font-size: 50px; /* Al ser una fuente, el tamaño se cambia con font-size */
  color: var(--neon-pink);
  margin-bottom: 20px;
  filter: drop-shadow(2px 2px 0px #000);
}

.tile-title {
  color: var(--neon-yellow);
  /* Título amarillo neón */
  font-family: 'Bangers', cursive;
  font-size: 1.6rem;
  margin: 0 0 15px 0;
  letter-spacing: 1.5px;
  -webkit-text-stroke: 1px #000;
  text-shadow: 2px 2px 0px #000;
}

.tile-desc {
  color: #dae1e7;
  /* Texto de descripción gris claro */
  font-family: 'Roboto', sans-serif;
  font-size: 0.95rem;
  margin: 0;
  line-height: 1.4;
}

.menu-icon {
  font-size: 35px; /* Controla el tamaño de las 3 rayitas */
}

/* ================================================= */
/* 🏁 ESTILOS DEL MODAL (OVERLAY Y CAJA)             */
/* ================================================= */

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85); /* Fondo oscuro semitransparente */
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Asegura que se dibuje por encima de todo */
}

.modal-content {
  background: var(--panel-bg);
  padding: 30px;
  width: 90%;
  max-width: 500px;
  border: 5px solid var(--neon-blue); /* Borde neón azul */
  box-shadow: 12px 12px 0 #000, 0 0 30px rgba(0, 204, 255, 0.3);
}

.modal-title {
  font-family: 'Orbitron', sans-serif;
  color: var(--neon-blue);
  font-size: 1.8rem;
  margin-top: 0;
  margin-bottom: 25px;
  text-align: center;
  -webkit-text-stroke: 1px #000;
  text-shadow: 2px 2px 0 #000;
}

/* Formularios dentro del modal */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Dos columnas para los inputs */
  gap: 15px;
}

.upload-group {
  margin-top: 15px;
  grid-column: 1 / -1; /* Ocupa todo el ancho */
}

.file-input {
  background: #111;
  color: #fff;
  padding: 10px;
  border: 3px solid #000;
  width: 100%;
  cursor: pointer;
  font-family: 'Roboto', sans-serif;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

/* Botones del modal */
.cancel-btn, .save-btn {
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  padding: 10px 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.cancel-btn {
  background: #ff3366; /* Rojo para cancelar */
  color: #fff;
}

.save-btn {
  background: var(--neon-green); /* Verde para guardar */
  color: #000;
}

.cancel-btn:hover, .save-btn:hover {
  transform: translate(-3px, -3px);
}

/* Animación de entrada/salida de Vue */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>