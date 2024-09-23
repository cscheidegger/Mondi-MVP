async function updateProjectList(shouldScroll = false) {
    loadingIndicator = document.getElementById('loading-indicator');
    document.getElementById('lista-error').classList.add('hidden');
    listaClientes = document.getElementById('lista-clientes');
    listaClientes.classList.remove('hidden');

    if (shouldScroll) {
        // Scroll até a lista
        document.getElementById('lista-oportunidades').scrollIntoView({ behavior: 'smooth' });
    }

    try {
        loadingIndicator.classList.remove('hidden');

        // Chama a API usando fetch para obter a lista de clientes
        const response = await fetch('http://127.0.0.1:5000/clientes');

        // Verifica se a requisição foi bem-sucedida
        if (!response.ok) {
            throw new Error('Erro ao buscar clientes: ' + response.status);
        }

        // Converte a resposta para JSON
        const clientes = await response.json();

        // Exibe os clientes no console
        printClientList(clientes);

    } catch (error) {
        document.getElementById('lista-error').classList.remove('hidden');
        console.error('Erro ao chamar a API:', error);
    } finally {
        loadingIndicator.classList.add('hidden');
    }
}

function printClientList(clientes) {
    const oportunidades = document.getElementById('lista-oportunidades');
    oportunidades.classList.remove('hidden');

    if (clientes.length === 0) {
        oportunidades.classList.add('hidden');
        return;
    }

    const container = document.getElementById('lista-clientes');
    clientes.forEach(cliente => {
        // Cria o div para cada cliente
        const clienteDiv = document.createElement('div');
        clienteDiv.classList.add('cliente');

        // Cria e adiciona o nome do cliente
        const nome = document.createElement('h2');
        nome.textContent = cliente.nome;
        clienteDiv.appendChild(nome);

        // Cria e adiciona o ID do cliente
        const id = document.createElement('p');
        id.textContent = `ID: ${cliente.id}`;
        clienteDiv.appendChild(id);

        // Cria e adiciona o email do cliente
        const email = document.createElement('p');
        email.textContent = `e-mail: ${cliente.email}`;
        clienteDiv.appendChild(email);

        // Cria e adiciona o tipo de projeto
        const tipoProjeto = document.createElement('p');
        tipoProjeto.textContent = `Tipo de Projeto: ${cliente.tipo_projeto}`;
        clienteDiv.appendChild(tipoProjeto);

        // Cria e adiciona a urgência
        const urgencia = document.createElement('p');
        urgencia.textContent = `Urgência: ${cliente.urgencia}`;
        clienteDiv.appendChild(urgencia);

        // Cria e adiciona a descrição
        const descricao = document.createElement('p');
        descricao.textContent = `Descrição: ${cliente.descricao}`;
        clienteDiv.appendChild(descricao);

        // Cria e adiciona a referência (caso exista)
        if (cliente.referencia) {
            const referencia = document.createElement('a');
            referencia.textContent = 'Referência';
            referencia.href = `uploads/${cliente.referencia}`;
            referencia.target = '_blank';
            clienteDiv.appendChild(referencia);
        }

        // Adiciona o div do cliente ao container principal
        container.appendChild(clienteDiv);
    });
}

// Listener para o evento de submissão do formulário
document.getElementById('form-cadastro').addEventListener('submit', function (e) {
    e.preventDefault();  // Previne o comportamento padrão de recarregar a página

    // Captura os DOM dos campos do formulário
    let nome = document.getElementById('nome');
    let tipo_projeto = document.getElementById('tipo_projeto');
    let urgencia = document.getElementById('urgencia');
    let descricao = document.getElementById('descricao');
    let email = document.getElementById('email');
    let referencia = document.getElementById('referencia');

    // Validação do formato do e-mail usando Regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value.trim())) {
        // Exibe mensagem de erro se o e-mail for inválido
        email.classList.add('error-border');
        document.getElementById('email-error').classList.remove('hidden');
        return;
    } else {
        // Esconde a mensagem de erro se o e-mail for válido
        email.classList.remove('error-border');
        document.getElementById('email-error').classList.add('hidden');
    }

    // Cria um objeto FormData para enviar os dados
    let formData = new FormData();
    formData.append('nome', nome.value.trim());
    formData.append('tipo_projeto', tipo_projeto.value);
    formData.append('urgencia', urgencia.value);
    formData.append('email', email.value.trim());
    formData.append('descricao', descricao.value);
    formData.append('referencia', referencia.files[0]);

    // Envia os dados para o backend usando fetch
    fetch('http://127.0.0.1:5000/cadastrar_cliente', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())  // Converte a resposta em JSON
        .then(data => {
            // Se a resposta contiver a mensagem de sucesso
            if (data.message) {
                // Exibe a mensagem de sucesso
                document.getElementById('mensagem-sucesso').classList.remove('hidden');
                // Limpa o formulário
                document.getElementById('form-cadastro').reset();
                // Atualiza a lista
                updateProjectList(true);
            }
        })
        .catch(error => {
            console.error("Erro ao enviar os dados:", error);  // Exibe erro no console se houver problema
        });
});

updateProjectList();