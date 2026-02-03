<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// O useRouter permite navegar entre páginas via código (ex: após logout)
const router = useRouter()

// Acesso à store global do Pinia para pegar dados do usuário sem precisar de props
const authStore = useAuthStore()

function realizarLogout() {
  // Limpa o token e o localStorage antes de redirecionar para a tela de login
  authStore.logout()
  router.push('/')
}
</script>

<template>
  <header class="main-header">
    <div class="header-content">
      <nav class="nav-links">
        <!-- O router-link é usado no lugar da tag <a> para evitar o reload da página,
             mantendo a performance de uma Single Page Application (SPA) -->
        <router-link to="/manutencao" class="link-item">Nova OS</router-link>
        <router-link to="/historico" class="link-item">Histórico</router-link>
      </nav>
      <div class="user-area">
        <!-- O nome do usuário é reativo; se mudar na store, atualiza aqui automaticamente -->
        <span class="welcome-text">Olá, <strong>{{ authStore.userName }}</strong></span>
        <button class="btn-logout" @click="realizarLogout">Sair</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* O "scoped" garante que este CSS não "vaze" para outros componentes do sistema */
.main-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  /* Fixa o cabeçalho no topo para que o usuário sempre tenha acesso à navegação ao rolar a página */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.link-item {
  color: #bdc3c7;
  text-decoration: none;
  font-weight: bold;
}

/* O Vue Router adiciona automaticamente a classe .router-link-active ao link da página atual */
.link-item:hover, .router-link-active {
  color: #2ecc71;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-text {
  font-size: 14px;
}

.btn-logout {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-logout:hover {
  background-color: #c0392b;
}
</style>
