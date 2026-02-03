import { defineStore } from 'pinia'
import axios from 'axios'

// Captura a URL da API definida no arquivo .env para facilitar a manutenção entre ambientes
const API_URL = import.meta.env.VITE_API_URL

export const useAuthStore = defineStore('auth', {
  /**
   * O Estado (State) guarda os dados na memória RAM da aplicação.
   * Inicializamos tentando buscar do localStorage para que, se o usuário der F5,
   * o sistema não perca os dados de login.
   */
  state: () => ({
    token: localStorage.getItem('token') || null,
    userEmail: localStorage.getItem('userEmail') || null,
    userName: localStorage.getItem('userName') || null,
  }),

  getters: {
    // Transforma a presença do token em um valor booleano (true/false) para as Guardas de Rota
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    /**
     * Realiza o login, guarda os dados na Store (memória) e no localStorage (disco).
     */
    async login(email, password) {
      try {
        const response = await axios.post(`${API_URL}/auth/login`, {
          email: email,
          senha: password, // Alinhado com o campo 'senha' definido no Schema do Backend
        })

        // Atualiza os dados na memória da aplicação
        this.token = response.data.access_token
        this.userEmail = response.data.user_email
        this.userName = response.data.user_name

        // Persistência: salva no navegador para manter a sessão ativa
        localStorage.setItem('token', this.token)
        localStorage.setItem('userEmail', this.userEmail)
        localStorage.setItem('userName', this.userName)

        // Padrão de Projeto: Configura o cabeçalho global do Axios.
        // Assim, toda requisição feita daqui pra frente enviará o Token JWT automaticamente.
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        return true
      } catch (error) {
        console.error('Erro no login:', error)
        throw error
      }
    },

    /**
     * Limpa completamente a sessão do usuário.
     */
    logout() {
      // Limpa a memória
      this.token = null
      this.userEmail = null
      this.userName = null

      // Limpa o disco
      localStorage.removeItem('token')
      localStorage.removeItem('userEmail')
      localStorage.removeItem('userName')

      // Remove a autorização global para que chamadas futuras sejam negadas pela API
      delete axios.defaults.headers.common['Authorization']
    },

    /**
     * Envia os dados para a criação de um novo usuário no backend.
     */
    async register(name, email, password) {
      try {
        await axios.post(`${API_URL}/auth/register`, {
          name: name,
          email: email,
          password: password,
        })
        return true
      } catch (error) {
        console.error('Erro no registro:', error)
        throw error
      }
    },
  }
})
