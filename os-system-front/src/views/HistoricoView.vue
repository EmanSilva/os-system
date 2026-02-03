<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import AppHeader from '@/components/AppHeader.vue'

// Estado reativo para armazenar a lista de ordens vindas do banco
const ordens = ref([])
const router = useRouter()
const toast = useToast()
const API_URL = import.meta.env.VITE_API_URL

// Estados para controlar o Modal de confirmação de exclusão
const mostrarModal = ref(false)
const idParaExcluir = ref(null)

/**
 * Busca todas as ordens de serviço do usuário logado.
 * O Token JWT é enviado automaticamente pelo interceptor que configuramos no Axios.
 */
async function carregarOrdens() {
  try {
    const response = await axios.get(`${API_URL}/ordens-servico`)
    ordens.value = response.data
  } catch (e) {
    toast.error('Erro ao carregar histórico')
  }
}

/**
 * Primeira etapa da exclusão: apenas abre o modal e guarda o ID alvo.
 */
function prepararExclusao(id) {
  idParaExcluir.value = id
  mostrarModal.value = true
}

/**
 * Segunda etapa da exclusão: chamada real para a API.
 */
async function confirmarExclusao() {
  try {
    await axios.delete(`${API_URL}/ordens-servico/${idParaExcluir.value}`)
    toast.success('Ordem de serviço excluída!')
    mostrarModal.value = false // Fecha o modal após o sucesso
    carregarOrdens() // Recarrega a lista para atualizar a tela
  } catch (e) {
    toast.error('Erro ao excluir a OS')
  }
}

/**
 * Envia o usuário para a tela de manutenção, mas passando os dados da OS
 * dentro do estado da rota. Isso permite que a tela de manutenção
 * preencha os campos automaticamente para edição.
 */
function editarOS(os) {
  router.push({
    name: 'manutencao',
    // Usamos JSON.parse/stringify para criar uma cópia limpa do objeto e evitar
    // problemas de referência de memória entre telas.
    state: { editData: JSON.parse(JSON.stringify(os)) },
  })
}

// Hook de ciclo de vida: executa a busca assim que o componente é montado na tela
onMounted(carregarOrdens)
</script>

<template>
  <div class="page-container">
    <!-- Componente global de cabeçalho -->
    <AppHeader />

    <!-- Card base centralizado que segue o padrão visual do sistema -->
    <div class="base-card content-size">
      <h2>Meu Histórico de OS</h2>

      <!-- Renderização condicional para o caso de não haver dados -->
      <div v-if="ordens.length === 0" class="empty-msg">Nenhuma ordem de serviço encontrada.</div>

      <!-- Listagem dinâmica usando v-for -->
      <div v-else class="orders-list">
        <div v-for="os in ordens" :key="os.id" class="os-item-row">
          <div class="os-info">
            <!-- Formatação simples de data para o padrão brasileiro -->
            <span class="os-date">{{ new Date(os.data_criacao).toLocaleDateString() }}</span>
            <p class="os-desc">{{ os.descricao }}</p>
          </div>
          <div class="os-actions">
            <button @click="editarOS(os)" class="btn-edit">Editar</button>
            <button @click="prepararExclusao(os.id)" class="btn-delete">Excluir</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmação: implementado com um overlay que cobre toda a tela -->
    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Excluir Ordem de Serviço?</h3>
        <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
        <div class="modal-buttons">
          <button @click="mostrarModal = false" class="btn-cancel">Cancelar</button>
          <button @click="confirmarExclusao" class="btn-confirm">Sim, Excluir</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

/*
.page-wrapper {
  min-height: 100vh;
  background-color: #f0f2f5;
  padding-top: 80px;
}

.os-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.os-card {
  background: white;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
*/
.os-date {
  font-size: 12px;
  color: #7f8c8d;
}

.os-desc {
  margin: 5px 0 0 0;
  color: #2c3e50;
  font-weight: 500;
}

.os-actions {
  display: flex;
  gap: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Fundo escurecido */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin-top: 0;
  color: #2c3e50;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
}

.btn-cancel {
  background: #bdc3c7;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.btn-confirm {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.btn-confirm:hover {
  background: #c0392b;
}
.btn-cancel:hover {
  background: #95a5a6;
}

.os-item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.os-item-row:last-child {
  border-bottom: none;
}

.btn-edit {
  background: #3498db;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.btn-delete {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}
.empty-msg {
  text-align: center;
  color: #7f8c8d;
  margin-top: 40px;
}
</style>
