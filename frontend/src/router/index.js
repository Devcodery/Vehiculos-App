import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegistroUsuariosView from '@/views/RegistroUsuariosView.vue'
import { useAuthStore } from '@/stores/auth'
import MiCuentaView from '@/views/MiCuentaView.vue'
import ListaProductosView from '@/views/ListaProductosView.vue'

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
    }
  ]
})

// El "Guarda" del Router: si no hay token, te manda al login
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // A. Si la ruta requiere estar logueado y no lo estás -> Al Login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  // B. Si la ruta es solo para ADMINS y tu rol es otro -> Te mandamos al garaje
  if (to.meta.requiresAdmin && authStore.user?.rol !== 'admin') {
    alert("Acceso denegado: Solo para administradores.")
    return next('/')
  }

  // C. Si todo está bien, pasa
  next()
})

export default router