# 🌱 IaEco - Cálculo de Pegada de Carbono

![Status do Deploy](https://img.shields.io/badge/deploy-online-brightgreen)  
![Licença](https://img.shields.io/badge/license-MIT-blue.svg)

O **IaEco** é uma aplicação web para **cálculo e visualização da pegada de carbono**, baseada nos escopos do **GHG Protocol** (Escopos 1, 2 e 3). A proposta é facilitar a gestão de emissões por meio de uma interface simples, interativa e responsiva.

---

## ✅ Requisitos

- **Node.js** versão **16 ou superior**
- **npm** versão **8 ou superior**

---

## 🚀 Instalação e uso

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/iaeco-frontend.git
cd iaeco-frontend 
```

### 2. Clone o repositório:

```bash
npm install
```

### 3. Configure as variáveis de ambiente:

```bash
cp .env-example .env
```

Edite o arquivo **.env** e defina a URL da API do back-end:

```bash
VITE_API_URL=http://localhost:8000/api
```

### 4. Inicie o projeto:

```bash
npm run dev
```
A aplicação estará disponível em: http://localhost:5173

## 🧪 Scripts disponíveis

| Comando           | Descrição                                   |
| ----------------- | ------------------------------------------- |
| `npm run dev`     | Inicia o servidor de desenvolvimento        |
| `npm run build`   | Gera os arquivos otimizados para produção   |
| `npm run preview` | Serve o projeto em modo produção localmente |

## 📁 Estrutura do Projeto

.
├── src/
│   ├── assets/            # Imagens e outros arquivos estáticos
│   ├── Components/        # Componentes reutilizáveis da interface
│   ├── hooks/             # Hooks personalizados
│   ├── pages/             # Páginas principais da aplicação
│   ├── routes/            # Configuração das rotas da aplicação
│   ├── services/          # Configuração do Axios e integração com API
│   ├── utils/             # Funções utilitárias
│   ├── App.css            # Estilos globais
│   ├── App.jsx            # Componente principal
│   └── main.jsx           # Ponto de entrada da aplicação
├── .env                   # Configurações locais (não versionado)
├── .env-example           # Exemplo de variáveis de ambiente
├── .gitignore             # Arquivos/dirs ignorados pelo Git
├── eslint.config.js       # Configuração do ESLint
├── index.html             # HTML principal da aplicação
├── package.json           # Dependências e scripts do projeto
├── package-lock.json      # Versões exatas das dependências
├── postcss.config.js      # Configuração do PostCSS
├── tailwind.config.js     # Configuração do TailwindCSS
├── vite.config.js         # Configuração do Vite
└── README.md              # Este documento


## 🛠️ Tecnologias e Ferramentas
 - Vite — Empacotador moderno e ultra-rápido

 - React — Biblioteca para criação de interfaces de usuário

 - Axios — Cliente HTTP para requisições assíncronas

 - TailwindCSS (se aplicável) — Framework CSS utilitário

 - GHG Protocol — Framework para contabilização de emissões de carbono

## 🌍 Sobre o IaEco
O IaEco ajuda organizações e indivíduos a identificar, categorizar e monitorar suas emissões de carbono com base em atividades que se encaixam nos escopos e categorias do GHG Protocol. O objetivo é promover a transparência climática e incentivar ações sustentáveis com apoio de tecnologia acessível.

## 📄 Licença
Este projeto está sob a licença MIT.
