// src/stores/auth.js
import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
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
        localStorage.setItem('token', this.token)
        
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
    }
  }
})