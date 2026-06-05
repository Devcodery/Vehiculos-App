import axios from 'axios';
import router from '@/router';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("El token ha caducado. Expulsando a la pantalla de login...")
      
      localStorage.removeItem('token')
      
      router.push('/login')
    }
    
    return Promise.reject(error)
  }
)

export default api