import { defineStore } from 'pinia'
import api from '@/services/api'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      try {
        // FastAPI usa OAuth2, por eso enviamos un FormData
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)

        const response = await api.post('/token', formData)
        this.token = response.data.access_token
        this.user = response.data.user_data

        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return { success: true }
      } catch (error) {
        console.error('Error en el login:', error)
        return { success: false, error: 'Credenciales inválidas' }
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})