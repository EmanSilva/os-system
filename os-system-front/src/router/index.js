import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'
import ManutencaoView from '@/views/ManutencaoView.vue'
import RegisterView from '@/views/RegisterView.vue'
import HistoricoView from '@/views/HistoricoView.vue'

/**
 * Definição das rotas do sistema.
 * O uso do campo 'meta: { requiresAuth: true }' é utilizado para marcar quais páginas são privadas e exigem um token válido.
 */
const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
    path: '/registrar',
    name: 'registrar',
    component: RegisterView
  },
  {
    path: '/manutencao',
    name: 'manutencao',
    component: ManutencaoView,
    meta: { requiresAuth: true } // Protege a tela de criação/edição
  },
  {
    path: '/historico',
    name: 'historico',
    component: HistoricoView,
    meta: { requiresAuth: true } // Protege a tela de listagem
  }
]

const router = createRouter({
  // O createWebHistory utiliza a API de histórico do navegador para URLs limpas (sem #)
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

/**
 * Navigation Guard (Guarda de Navegação) Global.
 * Ele verifica se a página destino exige autenticação e se o usuário possui um token na Store.
 */
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Se a rota exige autenticação e o usuário não está autenticado...
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redireciona forçadamente para a página de login
    next('/')
  } else {
    // Caso contrário, permite que a navegação continue normalmente
    next()
  }
})

export default router
