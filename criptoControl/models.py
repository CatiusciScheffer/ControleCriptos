from criptoControl import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """
    Representa um usuário no sistema.

    A classe User mapeia para a tabela 'users' no banco de dados e contém as informações
    principais de um usuário, como nome de usuário, e-mail e a senha criptografada.
    Além disso, define o relacionamento com as carteiras associadas ao usuário, 
    permitindo acessar as carteiras através do atributo 'user_wallets'.

    Atributos:
        user_id (int): Identificador único do usuário (chave primária).
        username (str): Nome de usuário único e obrigatório.
        email (str): E-mail único e obrigatório.
        password_hash (str): Senha do usuário, armazenada de forma segura.
        user_wallets (list): Relacionamento de um para muitos com a tabela 'wallets', 
                             onde o usuário pode ter várias carteiras.

    Métodos:
        __repr__(self): Retorna uma representação legível do objeto User, exibindo o e-mail do usuário.
        get_id(self): Retorna o identificador único do usuário.
    """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    user_wallets = db.relationship('Wallet', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def get_id(self):
        return self.user_id
    

class Wallet(db.Model):
    """
    Representa uma carteira de um usuário no sistema.

    A classe Wallet mapeia para a tabela 'wallets' no banco de dados e contém informações
    sobre as carteiras de criptomoedas de um usuário, incluindo o nome, rede e status da carteira.
    Também define um relacionamento com a tabela 'WalletBalance', permitindo acessar os saldos
    das criptomoedas presentes na carteira.

    Atributos:
        wallet_id (int): Identificador único da carteira (chave primária).
        wallet_user_id (int): Identificador do usuário ao qual a carteira pertence (chave estrangeira para 'users').
        wallet_name (str): Nome da carteira, identificador único para o usuário.
        wallet_network (str): Rede da carteira (por exemplo, Bitcoin, Ethereum, etc.).
        wallet_status (str): Status da carteira (geralmente 'N' para ativa e 'I' para inativa).
        balances (list): Relacionamento de um para muitos com a tabela 'wallet_balances', 
                          representando os saldos de criptomoedas na carteira.

    Métodos:
        __repr__(self): Retorna uma representação legível do objeto Wallet, exibindo o nome da carteira.
    """
    __tablename__ = 'wallets'  # Corrigido aqui para 'wallets'
    wallet_id = db.Column(db.Integer, primary_key=True)
    wallet_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) 
    wallet_name = db.Column(db.String, nullable=False)
    wallet_network = db.Column(db.String, nullable=False)
    wallet_status = db.Column(db.String(1), nullable=False, default='N' )
    #balances = db.relationship('WalletBalance', backref='payment_wallet', lazy=True)
    # Relacionamento com WalletBalance
    balances = db.relationship('WalletBalance', back_populates='wallet')

class Cryptocurrency(db.Model):
    __tablename__ = 'cryptocurrencies'
    crypto_id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String, unique=True, nullable=False)
    crypto_symbol = db.Column(db.String, unique=True, nullable=False)
    crypto_status = db.Column(db.String(1), nullable=False, default='N') 
    # Relacionamento com WalletBalance
    balances = db.relationship('WalletBalance', back_populates='cryptocurrency')
    """
    Representa uma criptomoeda no sistema.

    A classe Cryptocurrency mapeia para a tabela 'cryptocurrencies' no banco de dados e contém 
    informações sobre as criptomoedas, incluindo nome, símbolo e status. Também define um relacionamento 
    com a tabela 'WalletBalance', permitindo acessar os saldos das criptomoedas nas carteiras dos usuários.

    Atributos:
        crypto_id (int): Identificador único da criptomoeda (chave primária).
        crypto_name (str): Nome da criptomoeda (ex: Bitcoin, Ethereum).
        crypto_symbol (str): Símbolo da criptomoeda (ex: BTC, ETH).
        crypto_status (str): Status da criptomoeda ('N' para ativa, 'I' para inativa).
        balances (list): Relacionamento de um para muitos com a tabela 'wallet_balances', 
                          representando os saldos da criptomoeda nas carteiras.

    Métodos:
        __repr__(self): Retorna uma representação legível do objeto Cryptocurrency, exibindo o nome e símbolo.
    """

class WalletBalance(db.Model):
    """
    Representa o saldo de uma criptomoeda em uma carteira de usuário.

    A classe WalletBalance mapeia para a tabela 'wallet_balances' no banco de dados e contém 
    informações sobre o saldo de uma criptomoeda específica em uma carteira, incluindo o valor do saldo. 
    A classe também define relacionamentos com as tabelas 'Wallet' e 'Cryptocurrency', permitindo 
    acessar os dados da carteira e da criptomoeda associada.

    Atributos:
        balance_id (int): Identificador único do saldo (chave primária).
        balance_wallet_id (int): Identificador da carteira associada ao saldo (chave estrangeira para a tabela 'wallets').
        balance_crypto_id (int): Identificador da criptomoeda associada ao saldo (chave estrangeira para a tabela 'cryptocurrencies').
        balance (float): Quantidade de criptomoeda disponível na carteira.

    Relacionamentos:
        wallet (Wallet): Relacionamento de muitos para um com a tabela 'wallets', permitindo acessar a carteira associada.
        cryptocurrency (Cryptocurrency): Relacionamento de muitos para um com a tabela 'cryptocurrencies', permitindo acessar a criptomoeda associada.

    Métodos:
        __repr__(self): Retorna uma representação legível do objeto WalletBalance, exibindo o identificador da carteira, criptomoeda e saldo.
    """
    __tablename__ = 'wallet_balances'

    balance_id = db.Column(db.Integer, primary_key=True)
    balance_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.wallet_id'), nullable=False)
    balance_crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    # Definindo relacionamentos
    wallet = db.relationship('Wallet', back_populates='balances')
    cryptocurrency = db.relationship('Cryptocurrency', back_populates='balances')


class Transaction(db.Model):
    """
    Representa uma transação financeira envolvendo criptomoedas entre carteiras.

    A classe Transaction mapeia para a tabela 'transactions' no banco de dados e armazena informações
    detalhadas sobre uma transação, como o tipo de transação, as carteiras de pagamento e recebimento, 
    as criptomoedas envolvidas no pagamento e recebimento, bem como as taxas associadas.

    Atributos:
        transactions_id (int): Identificador único da transação (chave primária).
        transaction_type (str): Tipo da transação (ex: 'Compra', 'Venda', 'Transferência', etc.).
        transaction_date (date): Data da transação (com valor padrão para a data atual).

        # Carteira de pagamento
        payment_wallet_id (int): Identificador da carteira de pagamento (chave estrangeira para a tabela 'wallets').
        payment_wallet (Wallet): Relacionamento com a carteira de pagamento.

        # Carteira de recebimento
        receiving_wallet_id (int): Identificador da carteira de recebimento (chave estrangeira para a tabela 'wallets').
        receiving_wallet (Wallet): Relacionamento com a carteira de recebimento.

        # Criptomoeda de pagamento
        crypto_payment_id (int): Identificador da criptomoeda paga (chave estrangeira para a tabela 'cryptocurrencies').
        crypto_payment (Cryptocurrency): Relacionamento com a criptomoeda de pagamento.
        crypto_payment_price (float): Preço da criptomoeda no momento do pagamento.
        crypto_payment_quantity (float): Quantidade de criptomoeda paga.
        total_paid (float): Valor total pago na transação.

        # Criptomoeda de recebimento
        crypto_receive_id (int): Identificador da criptomoeda recebida (chave estrangeira para a tabela 'cryptocurrencies').
        crypto_receive (Cryptocurrency): Relacionamento com a criptomoeda de recebimento.
        crypto_receive_price (float): Preço da criptomoeda no momento do recebimento.
        crypto_receive_quantity (float): Quantidade de criptomoeda recebida.
        total_received (float): Valor total recebido na transação.

        # Taxa da transação
        crypto_fee_id (int): Identificador da criptomoeda utilizada para o pagamento de taxas (chave estrangeira para a tabela 'cryptocurrencies').
        crypto_fee (Cryptocurrency): Relacionamento com a criptomoeda usada para a taxa.
        crypto_fee_price (float): Preço da criptomoeda utilizada para o pagamento de taxas.
        crypto_fee_quantity (float): Quantidade de criptomoeda usada para o pagamento de taxas.
        total_fee (float): Valor total da taxa da transação.

    Relacionamentos:
        payment_wallet (Wallet): Relacionamento de muitos para um com a tabela 'wallets', representando a carteira de pagamento.
        receiving_wallet (Wallet): Relacionamento de muitos para um com a tabela 'wallets', representando a carteira de recebimento.
        crypto_payment (Cryptocurrency): Relacionamento de muitos para um com a tabela 'cryptocurrencies', representando a criptomoeda paga.
        crypto_receive (Cryptocurrency): Relacionamento de muitos para um com a tabela 'cryptocurrencies', representando a criptomoeda recebida.
        crypto_fee (Cryptocurrency): Relacionamento de muitos para um com a tabela 'cryptocurrencies', representando a criptomoeda utilizada para o pagamento de taxas.

    Métodos:
        __repr__(self): Retorna uma representação legível da transação, exibindo o tipo e o identificador da transação.
    """
    __tablename__ = 'transactions'
    
    # Dados da transação
    transactions_id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    # Carteira de pagamento
    payment_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.wallet_id'), nullable=True)
    payment_wallet = db.relationship('Wallet', foreign_keys=[payment_wallet_id], backref='transactions')
    
    # Carteira de recebimento
    receiving_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.wallet_id'), nullable=True)
    receiving_wallet = db.relationship('Wallet', foreign_keys=[receiving_wallet_id], backref='received_transactions')

    # Cripto pagamento
    crypto_payment_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=True)
    crypto_payment = db.relationship('Cryptocurrency', foreign_keys=[crypto_payment_id])
    crypto_payment_price = db.Column(db.Float, nullable=True)
    crypto_payment_quantity = db.Column(db.Float, nullable=True)
    total_paid = db.Column(db.Float, nullable=True)
    
    # Cripto recebimento
    crypto_receive_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=True)
    crypto_receive = db.relationship('Cryptocurrency', foreign_keys=[crypto_receive_id])  # Corrigido para usar crypto_receive_id
    crypto_receive_price = db.Column(db.Float, nullable=True)
    crypto_receive_quantity = db.Column(db.Float, nullable=True)
    total_received = db.Column(db.Float, nullable=True)

    # Cripto taxa    
    crypto_fee_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=True)
    crypto_fee = db.relationship('Cryptocurrency', foreign_keys=[crypto_fee_id])
    crypto_fee_price = db.Column(db.Float, nullable=True)
    crypto_fee_quantity = db.Column(db.Float, nullable=True)
    total_fee = db.Column(db.Float, nullable=True)
    
    # date_inclu = db.Column(db.Date, nullable=True) preenchimento automático no banco por triggers
    # hora_inclu = db.Column(db.Time, nullable=True) preenchimento automático no banco por triggers


class Price(db.Model):
    """
    Representa o preço de uma criptomoeda em um momento específico.

    A classe Price mapeia para a tabela 'prices' no banco de dados e armazena informações sobre os preços
    das criptomoedas, incluindo o valor do preço, a data e hora da consulta, e o relacionamento com a criptomoeda
    a qual o preço se refere.

    Atributos:
        price_id (int): Identificador único do registro de preço (chave primária).
        price (float): Valor do preço da criptomoeda no momento da consulta.
        price_consult_datetime (str): Data e hora da consulta do preço, armazenado como uma string.
        price_crypto_id (int): Identificador da criptomoeda à qual o preço se refere (chave estrangeira para a tabela 'cryptocurrencies').
        price_cryptocurrency (Cryptocurrency): Relacionamento com a criptomoeda associada ao preço. Este atributo facilita a navegação entre os modelos no SQLAlchemy, mas não é armazenado diretamente no banco de dados.

    Relacionamentos:
        price_cryptocurrency (Cryptocurrency): Relacionamento de muitos para um com a tabela 'cryptocurrencies', representando a criptomoeda associada ao preço.

    Métodos:
        __repr__(self): Retorna uma representação legível do preço da criptomoeda, incluindo o nome da criptomoeda e o valor do preço.
    """
    __tablename__ = 'prices'
    price_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    price_consult_datetime = db.Column(db.String, nullable=False)#não mudar tipo!
    price_crypto_id = db.Column(db.Integer, db.ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    price_cryptocurrency = db.relationship('Cryptocurrency') #não aparece no banco, mas é uma abstração usada pelo SQLAlchemy para facilitar a navegação entre os modelos 


