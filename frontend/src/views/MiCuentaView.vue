<template>
    <div class="dashboard-wrapper">
        <header class="section-header cell-shaded">
            <h2 class="section-title">
                <i class="fa-solid fa-circle-user"></i> MI CUENTA
            </h2>
            <p class="role-badge">{{ authStore.user?.rol }}</p>
        </header>

        <div class="two-columns">
            <section class="form-container">
                <form @submit.prevent="actualizarPerfil" class="brutalist-form cell-shaded">
                    <h3 class="form-title">DATOS PERSONALES</h3>

                    <div class="input-group">
                        <label>NOMBRE MOSTRADO</label>
                        <input type="text" v-model="perfilForm.nombre" class="brutalist-input" required />
                    </div>

                    <div class="input-group">
                        <label>CORREO ELECTRÓNICO</label>
                        <input type="email" v-model="perfilForm.email" class="brutalist-input" required />
                    </div>

                    <div v-if="mensajePerfil" :class="['mensaje-alerta', tipoMensajePerfil]">
                        {{ mensajePerfil }}
                    </div>

                    <button type="submit" class="submit-btn profile-btn cell-shaded" :disabled="cargandoPerfil">
                        <i class="fa-solid fa-floppy-disk"></i> {{ cargandoPerfil ? 'GUARDANDO...' : 'ACTUALIZAR DATOS'
                        }}
                    </button>
                </form>
            </section>

            <section class="form-container">
                <form @submit.prevent="actualizarPassword" class="brutalist-form cell-shaded danger-zone">
                    <h3 class="form-title text-danger">SEGURIDAD</h3>

                    <div class="input-group">
                        <label class="text-danger">CONTRASEÑA ACTUAL</label>
                        <div class="password-wrapper">
                            <input :type="showPasswordActual ? 'text' : 'password'" v-model="passwordForm.password_actual"
                                class="brutalist-input danger-input" required placeholder="********" />
                            <button type="button" class="toggle-btn" @click="showPasswordActual = !showPasswordActual">
                                <Transition name="icon-fade" mode="out-in">
                                    <span :key="showPasswordActual" class="icon-span">
                                        <i v-if="showPasswordActual" class="fa-solid fa-eye-slash icon-svg"></i>
                                        <i v-else class="fa-solid fa-eye icon-svg"></i>
                                    </span>
                                </Transition>
                            </button>
                        </div>
                    </div>

                    <div class="input-group">
                        <label class="text-danger">NUEVA CONTRASEÑA</label>
                        <div class="password-wrapper">
                            <input :type="showPasswordNueva ? 'text' : 'password'" v-model="passwordForm.password_nueva"
                                class="brutalist-input danger-input" required placeholder="********" />
                            <button type="button" class="toggle-btn" @click="showPasswordNueva = !showPasswordNueva">
                                <Transition name="icon-fade" mode="out-in">
                                    <span :key="showPasswordNueva" class="icon-span">
                                        <i v-if="showPasswordNueva" class="fa-solid fa-eye-slash icon-svg"></i>
                                        <i v-else class="fa-solid fa-eye icon-svg"></i>
                                    </span>
                                </Transition>
                            </button>
                        </div>
                    </div>

                    <div class="input-group">
                        <label class="text-danger">CONFIRMAR NUEVA</label>
                        <div class="password-wrapper">
                            <input :type="showConfirmarPassword ? 'text' : 'password'" v-model="passwordForm.confirmar_password"
                                class="brutalist-input danger-input" required placeholder="********" />
                            <button type="button" class="toggle-btn" @click="showConfirmarPassword = !showConfirmarPassword">
                                <Transition name="icon-fade" mode="out-in">
                                    <span :key="showConfirmarPassword" class="icon-span">
                                        <i v-if="showConfirmarPassword" class="fa-solid fa-eye-slash icon-svg"></i>
                                        <i v-else class="fa-solid fa-eye icon-svg"></i>
                                    </span>
                                </Transition>
                            </button>
                        </div>
                    </div>

                    <div v-if="mensajePassword" :class="['mensaje-alerta', tipoMensajePassword]">
                        {{ mensajePassword }}
                    </div>

                    <button type="submit" class="submit-btn password-btn cell-shaded" :disabled="cargandoPassword">
                        <i class="fa-solid fa-key"></i> {{ cargandoPassword ? 'CAMBIANDO...' : 'CAMBIAR CONTRASEÑA' }}
                    </button>
                </form>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

const perfilForm = ref({
    nombre: '',
    email: ''
})
const cargandoPerfil = ref(false)
const mensajePerfil = ref('')
const tipoMensajePerfil = ref('')

const passwordForm = ref({
    password_actual: '',
    password_nueva: '',
    confirmar_password: ''
})
const showPasswordActual = ref(false)
const showPasswordNueva = ref(false)
const showConfirmarPassword = ref(false)
const cargandoPassword = ref(false)
const mensajePassword = ref('')
const tipoMensajePassword = ref('')

onMounted(() => {
    if (authStore.user) {
        perfilForm.value.nombre = authStore.user.nombre
        perfilForm.value.email = authStore.user.email
    }
})


const actualizarPerfil = async () => {
    cargandoPerfil.value = true
    mensajePerfil.value = ''

    try {
        const response = await api.patch('/usuarios/change', perfilForm.value)
        mensajePerfil.value = '¡Datos actualizados correctamente!'
        tipoMensajePerfil.value = 'exito'

        authStore.user.nombre = response.data.nombre
        authStore.user.email = response.data.email

    } catch (error) {
        mensajePerfil.value = error.response?.data?.detail || 'Error al actualizar.'
        tipoMensajePerfil.value = 'error'
    } finally {
        cargandoPerfil.value = false
    }
}

const actualizarPassword = async () => {
    if (passwordForm.value.password_nueva !== passwordForm.value.confirmar_password) {
        mensajePassword.value = 'Las contraseñas nuevas no coinciden.'
        tipoMensajePassword.value = 'error'
        return
    }
    cargandoPassword.value = true
    mensajePassword.value = ''

    try {
        await api.patch('/usuarios/change/password', passwordForm.value)
        mensajePassword.value = '¡Contraseña cambiada con éxito!'
        tipoMensajePassword.value = 'exito'

        passwordForm.value.password_actual = ''
        passwordForm.value.password_nueva = ''
        passwordForm.value.confirmar_password = ''

        showPasswordActual.value = false
        showPasswordNueva.value = false
        showConfirmarPassword.value = false

    } catch (error) {
        mensajePassword.value = error.response?.data?.detail || 'Error al cambiar la contraseña.'
        tipoMensajePassword.value = 'error'
    } finally {
        cargandoPassword.value = false
    }
}
</script>

<style scoped>
.dashboard-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.section-header {
    background: #00e5ff;
    padding: 15px 20px;
    margin-bottom: 30px;
    border: 4px solid #000;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.section-title {
    font-family: 'Bangers', cursive;
    font-size: 2.5rem;
    color: #000;
    margin: 0;
    letter-spacing: 2px;
}

.role-badge {
    background: #000;
    color: #00e5ff;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    padding: 5px 15px;
    text-transform: uppercase;
    margin: 0;
}

.two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}

@media (max-width: 800px) {
    .two-columns {
        grid-template-columns: 1fr;
    }
}

.brutalist-form {
    background: #111;
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    border: 4px solid #fff;
    box-shadow: 8px 8px 0px #fff;
    height: 100%;
}

.danger-zone {
    border-color: #ff3333;
    box-shadow: 8px 8px 0px #ff3333;
}

.form-title {
    font-family: 'Bangers', cursive;
    font-size: 1.8rem;
    color: #fff;
    margin: 0 0 10px 0;
    border-bottom: 2px dashed #555;
    padding-bottom: 10px;
}

.text-danger {
    color: #ff3333 !important;
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.input-group label {
    color: #00e5ff;
    font-family: 'Bangers', cursive;
    font-size: 1.3rem;
    letter-spacing: 1px;
}

.brutalist-input {
    background: #000;
    color: #fff;
    border: 3px solid #555;
    padding: 12px 15px;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    outline: none;
    transition: border-color 0.2s;
}

.brutalist-input:focus {
    border-color: #00e5ff;
}

.danger-input:focus {
    border-color: #ff3333;
}

.submit-btn {
    font-family: 'Bangers', cursive;
    font-size: 1.5rem;
    padding: 15px;
    border: 4px solid #000;
    cursor: pointer;
    margin-top: auto;
    
    transition: transform 0.1s, box-shadow 0.1s;
}

.profile-btn {
    background: #00e5ff;
    color: #000;
}

.profile-btn:hover:not(:disabled) {
    transform: translate(-3px, -3px);
    box-shadow: 6px 6px 0px #000;
}

.password-btn {
    background: #ff3333;
    color: #fff;
}

.password-btn:hover:not(:disabled) {
    transform: translate(-3px, -3px);
    box-shadow: 6px 6px 0px #000;
}

.submit-btn:disabled {
    background: #555;
    cursor: not-allowed;
}

.mensaje-alerta {
    padding: 15px;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    text-align: center;
    border: 3px solid #000;
}

.exito {
    background: #00ff66;
    color: #000;
}

.error {
    background: #ff3333;
    color: #fff;
}


.password-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;
}

.password-wrapper input {
    padding-right: 50px;
}

.toggle-btn {
    position: absolute;
    right: 10px;
    background: none;
    border: none;
    cursor: pointer;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
}


.icon-svg {
    font-size: 20px;
    color: #999;
    transition: color 0.3s ease;
    filter: drop-shadow(2px 2px 0 #000);
}

.toggle-btn:hover .icon-svg {
    color: #00e5ff;
}


.icon-span {
    display: inline-block;
}
.icon-fade-enter-active,
.icon-fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}
.icon-fade-enter-from,
.icon-fade-leave-to {
    opacity: 0;
    transform: rotate(-180deg) scale(0.5);
}
</style>