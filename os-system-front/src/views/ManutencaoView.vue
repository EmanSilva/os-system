<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import { useToast } from 'vue-toastification'

/**
 * Hook de notificações e roteamento.
 * useRoute é usado para observar a URL atual, enquanto useRouter é para navegação.
 */
const toast = useToast()
const router = useRouter()
const route = useRoute()

// Estados da Ordem de Serviço
const idEdicao = ref(null) // Se preenchido, indica que estamos em modo de EDIÇÃO
const descricao = ref('')
const fotoBase64 = ref(null) // Armazena a imagem convertida para texto (Base64) para o banco
const enviando = ref(false) // Controle de UI para evitar múltiplos envios
const carregandoChecklist = ref(true)
const checklist = ref([]) // Lista dinâmica que virá da API
const API_URL = import.meta.env.VITE_API_URL

/**
 * Busca a configuração de checklist padrão do banco de dados (Bootstrap).
 * Usado apenas quando estamos criando uma NOVA Ordem de Serviço.
 */
async function buscarChecklistPadrao() {
  carregandoChecklist.value = true
  try {
    const response = await axios.get(`${API_URL}/config/checklist`)
    checklist.value = response.data
  } catch (error) {
    // Fallback: garante que a tela não fique vazia se a API falhar
    checklist.value = [{ tarefa: 'Erro ao carregar itens', concluido: false }]
  } finally {
    carregandoChecklist.value = false
  }
}

/**
 * Lógica principal de inicialização da tela.
 * Verifica se existem dados de edição enviados via 'history.state' (vindo do Histórico).
 */
async function inicializarTela() {
  const state = window.history.state

  if (state && state.editData) {
    // MODO EDIÇÃO: Preenche os campos com os dados da OS existente
    const data = state.editData
    idEdicao.value = data.id
    descricao.value = data.descricao
    checklist.value = data.checklist
    fotoBase64.value = data.foto_base64
    carregandoChecklist.value = false
  } else {
    // MODO CRIAÇÃO: Limpa os campos e busca o checklist padrão
    idEdicao.value = null
    descricao.value = ''
    fotoBase64.value = null
    await buscarChecklistPadrao()
  }
}

// Inicializa a tela quando o componente é montado
onMounted(inicializarTela)

/**
 * Observador de Rota (Watcher).
 * Se o usuário estiver editando e clicar em "Nova OS",
 * a URL muda mas o componente é o mesmo. O watch detecta isso e reseta a tela.
 */
watch(
  () => route.fullPath,
  () => {
    if (!window.history.state.editData) {
      inicializarTela()
    }
  },
)

/**
 * Processamento de Imagem.
 * O navegador lê o arquivo binário e o converte em uma string DataURL (Base64).
 * Isso permite salvar a imagem diretamente no MongoDB como um campo de texto.
 */
function aoSelecionarFoto(event) {
  const arquivo = event.target.files[0]
  if (arquivo) {
    const reader = new FileReader()
    reader.onload = (e) => {
      fotoBase64.value = e.target.result // Resultado: "data:image/png;base64,..."
    }
    reader.readAsDataURL(arquivo)
  }
}

/**
 * Salva os dados (POST para novas, PUT para edições).
 * Aplica validações de negócio exigidas antes de disparar a requisição.
 */
async function salvarOrdemServico() {
  // Validação: Pelo menos um item do checklist deve estar marcado (Regra de Negócio)
  const algumItemMarcado = checklist.value.some(item => item.concluido);

  if (!descricao.value) return toast.warning("Descreva a atividade!");
  if (!algumItemMarcado) return toast.warning("Marque pelo menos um item do checklist!");
  if (!fotoBase64.value) return toast.warning("A foto de comprovação é obrigatória!");

  enviando.value = true;
  try {
    const payload = {
      descricao: descricao.value,
      checklist: checklist.value,
      foto_base64: fotoBase64.value
    };

    if (idEdicao.value) {
      // Atualiza OS existente
      await axios.put(`${API_URL}/ordens-servico/${idEdicao.value}`, payload);
      toast.success("OS atualizada!");
    } else {
      // Cria nova OS
      await axios.post(`${API_URL}/ordens-servico`, payload);
      toast.success("OS enviada com sucesso!");
    }
    router.push('/historico'); // Redireciona para ver o resultado no histórico
  } catch (error) {
    // Captura mensagens de erro específicas vindas da validação do Pydantic (Backend)
    const erroAPI = error.response?.data?.detail[0]?.msg;
    toast.error(erroAPI || "Erro ao salvar OS.");
  } finally {
    enviando.value = false;
  }
}
</script>

<template>
  <div class="page-wrapper">
    <!-- Cabeçalho reutilizável contendo navegação e logout -->
    <AppHeader />

    <main class="content">
      <div class="os-container">
        <!-- Título Dinâmico baseado no estado da tela -->
        <h2>{{ idEdicao ? 'Editar Ordem de Serviço' : 'Nova Ordem de Serviço' }}</h2>

        <div class="section">
          <label>Descrição das Atividades:</label>
          <textarea
            v-model="descricao"
            placeholder="O que foi feito?"
            rows="4"
            :disabled="enviando"
          ></textarea>
        </div>

        <div class="section">
          <label>Checklist de Manutenção:</label>
          <p v-if="carregandoChecklist">Carregando tarefas...</p>
          <!-- Renderização de lista dinâmica vinda do Banco de Dados -->
          <div v-else v-for="(item, index) in checklist" :key="index" class="checklist-item">
            <input type="checkbox" v-model="item.concluido" :id="'item-' + index" />
            <label :for="'item-' + index">{{ item.tarefa }}</label>
          </div>
        </div>

        <div class="section">
          <label>Comprovação por Foto:</label>
          <!-- Atributo 'capture' sugere a abertura da câmera em dispositivos móveis -->
          <input
            type="file"
            accept="image/*"
            capture="environment"
            @change="aoSelecionarFoto"
            :disabled="enviando"
          />
          <!-- Preview da imagem antes do envio -->
          <div v-if="fotoBase64" class="preview-container">
            <p>Foto anexada:</p>
            <img :src="fotoBase64" alt="Preview" class="foto-img" />
          </div>
        </div>

        <!-- O botão muda de texto e cor conforme o contexto de edição/criação -->
        <button class="btn-salvar" @click="salvarOrdemServico" :disabled="enviando">
          {{ enviando ? 'Processando...' : idEdicao ? 'Atualizar OS' : 'Finalizar e Salvar OS' }}
        </button>

        <button v-if="idEdicao" @click="router.push('/historico')" class="btn-cancelar">
          Cancelar Edição
        </button>
      </div>
    </main>
  </div>
</template>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  width: 100%;
  background-color: #f0f2f5;
  display: flex;
  flex-direction: column;
  padding-top: 80px;
}

.content {
  flex: 1;
  padding: 20px;
}

.os-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.section {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 8px;
}

textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 0;
}

.preview-container {
  margin-top: 15px;
}

.foto-img {
  width: 100%;
  max-height: 250px;
  object-fit: contain;
  border: 1px solid #eee;
  border-radius: 4px;
}

.btn-salvar {
  width: 100%;
  padding: 15px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 10px;
}

.btn-salvar:hover {
  background-color: #27ae60;
}

.btn-cancelar {
  width: 100%;
  background: none;
  border: 1px solid #95a5a6;
  color: #7f8c8d;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-salvar:disabled {
  background-color: #95a5a6;
}
</style>
