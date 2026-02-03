<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from "vue-toastification";

const toast = useToast();
const authStore = useAuthStore()
const router = useRouter()

// Estados reativos para os campos de cadastro
const nome = ref('')
const email = ref('')
const senha = ref('')
const carregando = ref(false)

/**
 * Realiza o cadastro do técnico no sistema.
 * Aplica validações de segurança tanto no front quanto no tratamento do erro do back.
 */
async function realizarCadastro() {
  // 1. Validação: Impede a requisição se a senha for visivelmente fraca.
  // Regra: Mínimo 8 caracteres, pelo menos uma Letra Maiúscula e um Número.
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

  if (!nome.value || !email.value || !senha.value) {
    return toast.warning('Preencha todos os campos!');
  }

  if (!passwordRegex.test(senha.value)) {
    return toast.error('Senha fraca! Use 8+ caracteres, com uma letra maiúscula e um número.');
  }

  carregando.value = true;
  try {
    // Chama a action de registro definida na Store do Pinia
    await authStore.register(nome.value, email.value, senha.value);
    toast.success('Conta criada com sucesso!');
    router.push('/'); // Redireciona para o login após o sucesso
  } catch (e) {
    /**
     * TRATAMENTO DE ERRO REFINADO:
     * O FastAPI/Pydantic retorna erros de validação.
     * Aqui extraímos a mensagem e a transformamos em algo amigável para o usuário.
     */
    if (e.response && e.response.data && e.response.data.detail) {
      let apiMsg = e.response.data.detail[0].msg;

      // O Pydantic costuma incluir o prefixo "Value error, ", removemos para o Toast ficar limpo
      apiMsg = apiMsg.replace('Value error, ', '');

      toast.error(apiMsg);
    } else {
      // Fallback para erros de rede ou e-mail já cadastrado
      toast.error('Erro ao criar conta. Verifique os dados ou tente outro e-mail.');
    }
  } finally {
    carregando.value = false;
  }
}
</script>

<template>
  <!-- Classe global 'page-container' que centraliza o conteúdo em todas as telas -->
  <div class="page-container">

    <!-- 'base-card' e 'auth-size' são classes globais que mantêm a coerência visual do sistema -->
    <div class="base-card auth-size">
      <h1>Criar Conta</h1>

      <div class="form-group">
        <label>Nome Completo:</label>
        <input v-model="nome" type="text" placeholder="Seu nome" :disabled="carregando">
      </div>

      <div class="form-group">
        <label>E-mail:</label>
        <input v-model="email" type="email" placeholder="seu@email.com" :disabled="carregando">
      </div>

      <div class="form-group">
        <label>Senha:</label>
        <input v-model="senha" type="password" placeholder="Mínimo 8 caracteres" :disabled="carregando">
      </div>

      <button class="btn-primary" @click="realizarCadastro" :disabled="carregando">
        {{ carregando ? 'Processando...' : 'Cadastrar' }}
      </button>

      <div class="footer-link">
        Já tem uma conta? <router-link to="/">Entrar aqui</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>

.footer-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.footer-link a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
