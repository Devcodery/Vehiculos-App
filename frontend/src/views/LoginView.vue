<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h1>AutoCare</h1>
      
      <div class="input-group">
        <label>Email:</label>
        <input v-model="email" type="email" required placeholder="tu@email.com" />
      </div>

      <div class="input-group">
        <label>Contraseña:</label>
        <div class="password-wrapper">
          <input 
            v-model="password" 
            :type="showPassword ? 'text' : 'password'" 
            required 
            placeholder="••••••••"
          />
          
          <button 
            type="button" 
            class="toggle-btn" 
            @click="showPassword = !showPassword"
          >
            <Transition name="icon-fade" mode="out-in">
              <span :key="showPassword" class="icon-span">
                
                <svg v-if="showPassword" class="icon-svg" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>

                <svg v-else class="icon-svg" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>

              </span>
            </Transition>
          </button>
        </div>
      </div>

      <button type="submit" class="login-btn" :disabled="loading">
        {{ loading ? 'Entrando...' : 'Iniciar Sesión' }}
      </button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

// 1. Variables reactivas (lo que escribes en los cuadros)
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const authStore = useAuthStore()
const router = useRouter()

// 2. La función que se ejecuta al dar click al botón
const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  // Llamamos a la "acción" de la Store que creamos antes
  const result = await authStore.login(email.value, password.value)

  if (result.success) {
    // Si sale bien, nos vamos a la Home
    router.push('/')
  } else {
    // Si sale mal, mostramos el error
    errorMessage.value = result.error
  }
  loading.value = false
}
</script>

<style scoped>
/* 1. Importamos fuentes de Google: Una muy "Racing" para títulos y otra agresiva de cómic para el resto */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:ital,wght@0,700;1,900&family=Bangers&family=Roboto:wght@400;500&display=swap');

/* Clase útil global para aplicar el estilo "dibujado a mano" o "cell-shaded" */
.cell-shaded {
  border: 4px solid #000;
  box-shadow: 6px 6px 0 #000;
}

.login-container {
  /* Variables de color de nuestro diseño comic-gamberro */
  --neon-yellow: #fff200;
  --neon-blue: #00ccff;
  --neon-pink: #ff00ff;
  --dark-bg: #0b0c10;
  --panel-bg: rgba(15, 20, 25, 0.9);

  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Ocupamos toda la pantalla */
  
  font-family: 'Roboto', sans-serif;
}

.login-form {
  background: var(--panel-bg);
  padding: 3rem;
  /* 3. Estilo cell-shaded: Borde grueso y sombra de cómic */
  border: 5px solid #000;
  box-shadow: 10px 10px 0 #000, 0 0 20px rgba(0, 255, 102, 0.15);
  border-radius: 4px;
  width: 340px;
  backdrop-filter: blur(8px);
  /* Esquina de la caja "abollada" con neón */
  position: relative;
  overflow: hidden;
}

.login-form::before {
  content: "ZAP!";
  font-family: 'Bangers', cursive;
  font-size: 1.2rem;
  color: var(--neon-pink);
  position: absolute;
  top: -10px;
  right: -10px;
  transform: rotate(15deg);
}

h1 {
  /* 4. Tipografía "Racing" itálica de Orbitron con contorno negro */
  font-family: 'Orbitron', sans-serif;
  font-style: italic;
  font-weight: 900;
  text-transform: uppercase;
  font-size: 2.2rem;
  text-align: center;
  margin-bottom: 2.5rem;
  letter-spacing: 3px;
  /* Texto azul brillante con contorno negro */
  color: var(--neon-blue);
  -webkit-text-stroke: 1.5px #000; /* Contorno negro para el texto */
  text-shadow: 3px 3px 0 #000, 0 0 10px rgba(0, 204, 255, 0.6);
}

.input-group {
  margin-bottom: 1.8rem;
}

label {
  display: block;
  font-family: 'Bangers', cursive; /* Fuente agresiva de cómic */
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #fff;
  margin-bottom: 8px;
}

input {
  width: 100%;
  padding: 14px;
  /* Inputs de "metal abollado" con textura de semitono */
  background: rgba(0, 0, 0, 0.7);
  background-image: radial-gradient(#333 10%, transparent 11%), radial-gradient(#333 10%, transparent 11%);
  background-size: 10px 10px;
  background-position: 0 0, 5px 5px;
  border: 4px solid #000; /* Estilo cell-shaded */
  border-radius: 2px;
  color: #fff;
  font-size: 1.1rem;
  font-family: 'Roboto', sans-serif;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

/* 5. Efecto al hacer clic en un input: Se enciende en neón rosa */
input:focus {
  border-color: var(--neon-pink);
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
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

/* Adaptamos los iconos SVG para que se vean bien y más "sucios" */
.icon-svg {
  width: 24px;
  height: 24px;
  color: #999;
  transition: color 0.3s ease;
  filter: drop-shadow(2px 2px 0 #000);
}

.toggle-btn:hover .icon-svg {
  color: var(--neon-blue); /* Brilla en azul al pasar el ratón */
}

/* 6. El botón de Iniciar Sesión estilo Explosión */
.login-btn {
  width: 100%;
  padding: 15px;
  margin-top: 15px;
  background-color: var(--neon-yellow);
  background-image: 
    repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0,0,0,0.1) 10px, rgba(0,0,0,0.1) 20px);
  color: #000;
  font-family: 'Orbitron', sans-serif;
  font-weight: 900;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  /* Estilo cell-shaded agresivo */
  border: 5px solid #000;
  border-radius: 4px;
  box-shadow: 6px 6px 0 #000, 0 0 15px rgba(255, 242, 0, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover:not(:disabled) {
  transform: translate(-3px, -3px); /* Hace un pequeño gesto de "salto" de viñeta */
  box-shadow: 9px 9px 0 #000, 0 0 25px rgba(255, 242, 0, 0.7);
}

.login-btn:disabled {
  background: #333;
  color: #666;
  border-color: #666;
  box-shadow: none;
  cursor: not-allowed;
}

.error {
  font-family: 'Bangers', cursive;
  color: #ff3366; /* Un rojo neón para los errores */
  text-align: center;
  font-size: 1.1rem;
  margin-top: 20px;
  text-shadow: 3px 3px 0 #000;
}

/* Mantén las clases de transición de los iconos que hicimos antes */
.icon-span { display: inline-block; }
.icon-fade-enter-active, .icon-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.icon-fade-enter-from, .icon-fade-leave-to { opacity: 0; transform: rotate(-180deg) scale(0.5); }
</style>