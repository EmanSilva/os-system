<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from "vue-toastification";

// Inicialização dos hooks
const toast = useToast();
const authStore = useAuthStore()
const router = useRouter()

// Estados reativos (refs) que serão vinculados aos inputs via v-model
const email = ref('')
const senha = ref('')

// Estado de controle para desabilitar o botão e inputs durante a requisição (evita múltiplos cliques)
const carregando = ref(false)

async function realizarLogin() {
  // Validação simples de Front-end para evitar chamadas inúteis à API
  if (!email.value || !senha.value) {
    toast.info("Preencha todos os campos para entrar.");
    return;
  }

  carregando.value = true

  try {
    // Chamada da action de login na Store. A Store encapsula a lógica de requisição HTTP.
    const sucesso = await authStore.login(email.value, senha.value)

    if (sucesso) {
      toast.success("Login realizado com sucesso!");
      // Redirecionamento programático para a área restrita
      router.push('/manutencao')
    }
  } catch (e) {
    // Tratamento de erro centralizado para falhas de autenticação
    toast.error("E-mail ou senha incorretos. Tente novamente.");
    console.error("Erro no login:", e);
  } finally {
    // Garante que o estado de carregamento seja desativado independente do sucesso ou erro
    carregando.value = false
  }
}
</script>

<template>
  <!-- Container principal centralizado via CSS global -->
  <div class="login-container">
    <h1>Acesso ao Sistema</h1>

    <!-- Nota: O uso do v-model cria uma ligação de via dupla (Two-way data binding)
         entre o input HTML e a variável ref no JavaScript -->
    <div class="form-group">
      <label>E-mail:</label>
      <input
        v-model="email"
        type="email"
        placeholder="técnico@exemplo.com"
        :disabled="carregando"
      >
    </div>

    <div class="form-group">
      <label>Senha:</label>
      <input
        v-model="senha"
        type="password"
        placeholder="Sua senha"
        :disabled="carregando"
      >
    </div>

    <!-- O atributo :disabled impede que o usuário envie o formulário várias vezes seguidas -->
    <button @click="realizarLogin" :disabled="carregando">
      {{ carregando ? 'Entrando...' : 'Entrar' }}
    </button>

    <div class="footer-link">
      <!-- O router-link permite a navegação interna sem recarregar a página inteira -->
      Não tem uma conta? <router-link to="/registrar">Cadastre-se aqui</router-link>
    </div>
  </div>
</template>

<style scoped>
/* Estilos isolados para este componente.
   O 'scoped' evita que estes seletores afetem outros botões ou inputs do site */
.login-container {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h1 {
  text-align: center;
  color: #1a1a1a;
  font-size: 24px;
  margin-bottom: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: 600;
  color: #4a4a4a;
}

input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus {
  border-color: #42b983; /* Cor verde característica do Vue */
  outline: none;
}

button {
  padding: 14px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #38a169;
}

/* Estado visual para quando o botão está processando a requisição */
button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.footer-link {
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
}

.footer-link a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}
</style>
