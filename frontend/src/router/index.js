import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegistroUsuariosView from '@/views/RegistroUsuariosView.vue'
import { useAuthStore } from '@/stores/auth'
import MiCuentaView from '@/views/MiCuentaView.vue'
import ListaProductosView from '@/views/ListaProductosView.vue'
import ServiciosView from '@/views/ServiciosView.vue'
import TipoServicioView from '@/views/TipoServicioView.vue'
import VehiculoDetalleView from '@/views/VehiculoDetalleView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/',
      name: 'Home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/registro-usuarios',
      name: 'RegistroUsuarios',
      component: RegistroUsuariosView,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/mi-cuenta',
      name: 'MiCuenta',
      component: MiCuentaView,
      meta: {requiresAuth: true}
    },
    {
      path: '/lista-productos',
      name: 'ListaProductos',
      component: ListaProductosView,
      meta: {requiresAuth: true}
    },
    {
      path: '/historial-servicios',
      name: 'HistorialServicios',
      component: ServiciosView,
      meta: {requiresAuth: true}
    },
    {
      path: '/tipos-servicios',
      name: 'TiposServicio',
      component: TipoServicioView,
      meta: {requiresAuth: true}
    },
    {
      path: '/vehiculo/:id',
      name: 'VehiculoDetalle',
      component: VehiculoDetalleView,
      meta: {requiresAuth: true}
    }
  ]
})

router.beforeEach((to, from) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login'
  }

  if (to.meta.requiresAdmin && authStore.user?.rol !== 'admin') {
    alert("Acceso denegado: Solo para administradores.")
    return '/'
  }
})

export default router