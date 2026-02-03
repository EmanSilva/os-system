import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

/**
 * IMPORTAÇÃO DE PLUGINS
 * Toastification é usado para exibir notificações (Toasts) de forma global.
 */
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

// Criação da instância principal da aplicação Vue
const app = createApp(App)

// Injeção dos plugins essenciais na aplicação
app.use(createPinia()) // Gerenciador de estado global (Pinia)
app.use(router)      // Sistema de roteamento (Vue Router)

/**
 * CONFIGURAÇÃO GLOBAL DE NOTIFICAÇÕES
 * Define o comportamento padrão dos alertas visuais do sistema.
 */
app.use(Toast, {
    transition: "Vue-Toastification__bounce",
    maxToasts: 5,
    newestOnTop: true
});

/**
 * PADRÃO DE PERSISTÊNCIA DE AUTENTICAÇÃO
 * Verifica se existe um Token JWT no localStorage
 * assim que o app é carregado (ex: após um F5).
 * Se o token existir, ele o injeta nos cabeçalhos padrão do Axios para que
 * o usuário não precise logar novamente e todas as requisições sejam autorizadas.
 */
const token = localStorage.getItem('token')
if (token) {
    // Configura o cabeçalho 'Authorization' globalmente para todas as chamadas da API
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

/**
 * MONTAGEM DA APLICAÇÃO
 * Conecta a instância do Vue ao elemento HTML com ID 'app' (definido no index.html).
 */
app.mount('#app')
