# gestao-mondi-mvp-tmp

# Mondi Cadastro

Este projeto é uma aplicação de cadastro de clientes desenvolvida para a Mondi Arquitetura. A aplicação permite que os clientes se registrem com informações sobre nome, telefone, e-mail, tipo de projeto e uma descrição da demanda.

## Objetivo

A aplicação foi desenvolvida para resolver o problema de organização e cadastro de clientes interessados em projetos arquitetônicos. Com a aplicação, a Mondi Arquitetura pode coletar e gerenciar informações de clientes interessados em projetos residenciais, comerciais e de ambientes.

## Funcionalidades

- **Formulário de Cadastro de Clientes**: Os usuários podem preencher um formulário com nome, telefone, e-mail, tipo de projeto e uma descrição da demanda.
- **Validações Básicas**: O e-mail é validado antes de o formulário ser submetido.
- **Banco de Dados**: Os dados dos clientes são salvos em um banco de dados SQLite.
- **Interface Responsiva**: A interface foi construída usando **Bootstrap** para ser compatível com dispositivos móveis e desktops.
  
## Tecnologias Utilizadas

- **Flask** (Python)
- **SQLite** (Banco de Dados)
- **HTML5**
- **CSS3** (Bootstrap para estilização)
- **JavaScript** (para validações e interações)

## Como Executar o Projeto

### Backend (API)

1. Clone o repositório

2. Navegue até a pasta do backend:
```bash
cd mondi-cadastro/backend
```

3. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
```

4. Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

5. Execute o servidor Flask:
```bash
python app.py
```

O app criará as tabelas no banco de dados automaticamente na inicialização caso elas não existam.

### Frontend (Interface do Usuário)

1. Acesse o formulário de cadastro no navegador:
Com o servidor Flask em execução, abra o navegador e acesse http://127.0.0.1:5000/.

2. Preencha e envie o formulário:
Preencha os campos do formulário e clique em "Submeter". Os dados serão enviados para o backend e salvos no banco de dados.
```
mondi-cadastro/
├── backend/
│   ├── app.py                    # Código do backend em Flask
│   ├── criar_tabela.py           # Script para criar a tabela de clientes
│   ├── db.sqlite                 # Banco de dados SQLite (gerado automaticamente)
│   ├── requirements.txt          # Lista de dependências do projeto
│   ├── uploads/                  # Pasta para salvar os arquivos enviados pelo formulário
└── frontend/
    ├── index.html                # Página HTML para o formulário de cadastro
    ├── static/
    │   ├── style.css             # Estilos personalizados
    │   ├── app.js                # Script JavaScript para validações e interações
    │   ├── Mondi_logo.png        # Logo da Mondi Arquitetura
```
