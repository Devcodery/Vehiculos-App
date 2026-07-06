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
                
                <i v-if="showPassword" class="fa-solid fa-eye-slash icon-svg"></i>

                <i v-else class="fa-solid fa-eye icon-svg"></i>

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

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  const result = await authStore.login(email.value, password.value)

  if (result.success) {
    router.push('/')
  } else {
    errorMessage.value = result.error
  }
  loading.value = false
}
</script>

<style scoped>

.cell-shaded {
  border: 4px solid #000;
  box-shadow: 6px 6px 0 #000;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; 
  
  font-family: 'Roboto', sans-serif;
}

.login-form {
  background: var(--panel-bg);
  padding: 3rem;
  
  border: 5px solid #000;
  box-shadow: 10px 10px 0 #000, 0 0 20px rgba(0, 255, 102, 0.15);
  border-radius: 4px;
  width: 340px;
  backdrop-filter: blur(8px);
  
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
  
  font-family: 'Orbitron', sans-serif;
  font-style: italic;
  font-weight: 900;
  text-transform: uppercase;
  font-size: 2.2rem;
  text-align: center;
  margin-bottom: 2.5rem;
  letter-spacing: 3px;
  
  color: var(--neon-blue);
  -webkit-text-stroke: 1.5px #000; 
  text-shadow: 3px 3px 0 #000, 0 0 10px rgba(0, 204, 255, 0.6);
}

.input-group {
  margin-bottom: 1.8rem;
}

label {
  display: block;
  font-family: 'Bangers', cursive; 
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #fff;
  margin-bottom: 8px;
}

input {
  width: 100%;
  padding: 14px;
  
  background: rgba(0, 0, 0, 0.7);
  background-image: radial-gradient(#333 10%, transparent 11%), radial-gradient(#333 10%, transparent 11%);
  background-size: 10px 10px;
  background-position: 0 0, 5px 5px;
  border: 4px solid #000; 
  border-radius: 2px;
  color: #fff;
  font-size: 1.1rem;
  font-family: 'Roboto', sans-serif;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}


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


.icon-svg {
  font-size: 20px; 
  color: #999;
  transition: color 0.3s ease;
  filter: drop-shadow(2px 2px 0 #000); 
}

.toggle-btn:hover .icon-svg {
  color: var(--neon-blue); 
}


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
  
  border: 5px solid #000;
  border-radius: 4px;
  box-shadow: 6px 6px 0 #000, 0 0 15px rgba(255, 242, 0, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover:not(:disabled) {
  transform: translate(-3px, -3px); 
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
  color: #ff3366; 
  text-align: center;
  font-size: 1.1rem;
  margin-top: 20px;
  text-shadow: 3px 3px 0 #000;
}


.icon-span { display: inline-block; }
.icon-fade-enter-active, .icon-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.icon-fade-enter-from, .icon-fade-leave-to { opacity: 0; transform: rotate(-180deg) scale(0.5); }
</style>