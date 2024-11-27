<h2>Gerenciador de Criptomoedas</h2> 
<p>Este é um aplicativo de gerenciamento de criptomoedas desenvolvido em Flask, projetado para ajudar usuários a rastrear suas transações, saldos e carteiras. Ele também fornece suporte para taxas e preços dinâmicos de criptomoedas. Ideal para entusiastas de cripto e traders!</p>

<h3>🚀 Funcionalidades</h3>
    Gerenciamento de carteiras: Crie, edite e exclua carteiras de criptomoedas.

    Controle de transações:
    
    Compra
    
    Venda
    
    Transferência
    
    Adição de saldo
    
    Atualização de preços: Integração com dados de preços de criptomoedas em tempo real, necessário solicitar a atualização clicando no botão específico.
    
    Relatórios detalhados: Exibição de histórico de transações com cálculos de taxas e totais.
    
    Verificação de saldo: Validações automáticas para evitar transações inválidas.
    
    Reversão de transações: Suporte para desfazer operações anteriores.
    
    Análises de DCA, Lucro e Prejuízo das trasações realizadas.

<h3>🛠️ Tecnologias Utilizadas</h3>

Backend: Flask, SQLAlchemy

Frontend: HTML, CSS, Bootstrap

Banco de Dados: SQLite

Outras bibliotecas:

Flask-WTF (validação de formulários)

WTForms (criação de formulários dinâmicos)

<h3>🗂️ Estrutura do Projeto</h3>

CRYPTOS_FLASK

    ├── criptoControl    
    │   ├── routes    
    │   │   ├── __init__.py
    │   │   ├── auth_routes.py
    │   │   ├── crud_crypto_wallet.py
    │   │   ├── main_routes.py
    │   │   ├── transactions_routes.py
    │   │   ├── update_price.py
    │   │   └── views_databases.py
    │   ├── static
    │   │   ├── css
    │   │   │   └── style.css
    │   │   ├── js
    │   │   │   ├── scripts_consulltaTransacoes.js
    │   │   │   └── scripts_transacoes.js
    │   ├── templates
    │   │   ├── auth
    │   │   │   └── login.html
    │   │   ├── operacoes
    │   │   │   ├── add_crypto.html
    │   │   │   ├── add_transactions.html
    │   │   │   ├── add_wallet.html
    │   │   │   ├── cryptos.html
    │   │   │   ├── modal_confirm_delete.html
    │   │   │   ├── transactions.html
    │   │   │   └── wallets.html
    │   │   ├── views_databases
    │   │   │   ├── crypto_DCA.html
    │   │   │   ├── crypto_lucroXprejuizo.html
    │   │   │   ├── filtros_transacoes.html
    │   │   │   ├── prices.html
    │   │   │   ├── transacoes_filtradas.html
    │   │   │   ├── wallet_ballances.html
    │   │   │   └── wallet_summary.html
    │   │   ├── index.html
    │   │   └── navibar.html
    │   ├── __init__.py
    │   ├── api.py
    │   ├── forms.py
    │   └── models.py
    ├── env
    ├── instance
    │   └── crypto_data.db
    ├── main.py
    └── requirements.txt


<h3>⚙️ Instalação e Execução</h3>
Clone o repositório:

git clone https://github.com/CatiusciScheffer/ControleCriptos
cd crypto-manager
Crie um ambiente virtual e instale as dependências:

python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure o banco de dados:

flask db init
flask db migrate
flask db upgrade
Execute o aplicativo:

flask run
Acesse no navegador: http://127.0.0.1:5000

<h3>📝 Contribuição</h3>
Contribuições são bem-vindas! Para contribuir:

Abra um Pull Request.
<h3>📜 Licença</h3>
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

<h3>📬 Contato</h3>

Se tiver dúvidas ou sugestões, entre em contato:

📧 cpcscheffer@outlook.com

🌐 Projeto hospedado: https://controlecripto-18636635ed0d.herokuapp.com/ (utilize para login: catiusci.ctadigital@gmail.com / senha Chefa220408#)

