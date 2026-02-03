# Prototipagem de Sistema de Ordem de Serviço (OS) 🛠️

Este projeto é uma plataforma para a gestão e execução de Ordens de Serviço (OS). O sistema abrange desde a autenticação até o registro detalhado de atividades, incluindo checklist dinâmico e comprovação fotográfica obrigatória.

## 🚀 Tecnologias e Ferramentas

### Backend (API)
- **Linguagem:** Python 3.11
- **Framework:** FastAPI (Assíncrono)
- **Banco de Dados:** MongoDB (NoSQL)
- **Driver:** Motor (Async MongoDB Driver)
- **Autenticação:** JWT (JSON Web Tokens) com criptografia `bcrypt`
- **Validação:** Pydantic V2 (DTOs e Schemas com validadores customizados)

### Frontend (Web)
- **Framework:** Vue.js 3
- **Gerenciamento de Estado:** Pinia
- **Navegação:** Vue Router
- **Comunicação:** Axios (com configuração global de Headers)
- **Interface:** CSS3 Moderno com Design Responsivo, Toasts (Vue-Toastification) e Modais de confirmação.

### Infraestrutura
- **Orquestração:** Docker & Docker Compose
- **Servidor Web Front:** Nginx (Alpine) para servir os arquivos estáticos do Vue.

## 🏗️ Padrões de Projeto e Arquitetura

O projeto foi elaborado para seguir padrões de mercado que visam a organização e o desacoplamento:

1.  **Arquitetura Modular (Backend):** 
    - **Repositories:** Isolam o acesso ao MongoDB.
    - **Services:** Centralizam a lógica de negócio e orquestração.
    - **Modular Routing:** Uso de `APIRouter` para separar os endpoints por responsabilidade (`auth`, `os`, `config`).
    - **DTO Pattern:** Uso de Schemas Pydantic para transferência e validação rigorosa de dados.
2.  **Singleton Pattern:** Gerenciamento eficiente da conexão com o banco de dados via instâncias compartilhadas pelo Motor.
3.  **Dependency Injection:** Uso do sistema de `Depends` do FastAPI para gerenciar instâncias de serviços e proteger rotas.
4.  **Component-Based UI:** Frontend modularizado em componentes reutilizáveis para garantir consistência visual e facilidade de manutenção.
5.  **Bootstrap Resiliente (Self-Healing):** A API utiliza o evento `lifespan` para garantir que o banco de dados seja auto-populado com o checklist mestre e um usuário administrador na primeira execução.


## 📋 Requisitos Implementados

- [x] **Autenticação JWT:** Login seguro com persistência de token no navegador.
- [x] **Gestão de Usuários:** Cadastro com validação rigorosa de e-mail e força de senha.
- [x] **Manutenção de OS:** Registro de descrição, checklist dinâmico e upload de foto.
- [x] **Checklist Dinâmico:** Carregado em tempo real a partir das configurações do banco.
- [x] **Histórico de OS:** Listagem completa com funcionalidades de **Edição** e **Exclusão** (CRUD).
- [x] **Navigation Guards:** Proteção de rotas no frontend, impedindo acesso de usuários não autenticados.
- [x] **Feedback ao Usuário:** Notificações via Toast para todas as ações e erros do sistema.


## 🛠️ Como Executar o Projeto

É necessário ter o **Docker** instalado em seu ambiente (Linux, macOS ou Windows).

### 1. Clonar o Repositório
```bash
git clone https://github.com/EmanSilva/os-system.git
cd os-system-prototype
```

### 2. Configurar Variáveis de Ambiente
O projeto utiliza arquivos `.env` para gerenciar endereços de banco e chaves de segurança. Exemplos funcionais já estão presentes para facilitar o deploy imediato.

### 3. Subir o Ambiente Completo
Na raiz do projeto, execute:
```bash
docker-compose up --build
```
*Este comando compila as imagens, configura a rede interna e sobe todos os serviços (API, Web, Banco).*

### 4. Acesso ao Sistema
- **Frontend (Vue):** [http://localhost:8080](http://localhost:8080)
- **Documentação API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Mongo Express (Admin Banco):** [http://localhost:8081](http://localhost:8081)

## 👤 Credenciais de Acesso Inicial

O sistema se auto-configura no primeiro deploy. Você pode utilizar os dados abaixo para o primeiro acesso:

- **E-mail:** `admin@teste.com`
- **Senha:** `123` *(O sistema permite criar novos usuários).*

Para acessar o Mongo Express, utilize:
- **User:** `admin`
- **Password:** `pass`


## 📂 Estrutura Principal do Repositório

```text
├── os-system-api/          # Backend Python (FastAPI)
│   ├── app/
│   │   ├── api/            # Rotas modulares
│   │   ├── core/           # Segurança, Configurações e Bootstrap
│   │   ├── repositories/   # Acesso ao MongoDB
│   │   ├── schemas/        # DTOs e Validações Pydantic
│   │   └── services/       # Lógica de Negócio
│   └── Dockerfile
├── os-system-front/        # Frontend Vue.js
│   ├── src/                # Componentes, Views e Pinia Stores
│   ├── Dockerfile          # Build de Produção
│   └── nginx.conf          # Configuração do Servidor Web
└── docker-compose.yml      # Orquestrador Geral
```

### 🛡️ Validações de Segurança
- **Senhas:** Devem ter no mínimo 8 caracteres, incluindo uma letra maiúscula e um número.
- **Integridade da OS:** O sistema bloqueia envios sem descrição, sem foto anexada ou sem pelo menos um item do checklist marcado.


### Desenvolvido por:
**Emanuel Oliveira**
[LinkedIn](https://www.linkedin.com/in/emanuel-oliveira-da-silva-386608123/) | [GitHub](https://github.com/seu-usuario)
