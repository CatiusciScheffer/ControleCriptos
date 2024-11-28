from flask import Blueprint, render_template, url_for, flash, request, redirect, session, jsonify, request
from criptoControl.forms import TransactionsForm, AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, WalletBalance, Transaction, Price
from flask_login import current_user, login_required
from sqlalchemy.orm import sessionmaker, joinedload
from datetime import datetime
from math import ceil


transaction_bp = Blueprint('transaction', __name__)

def create_session():
    return sessionmaker(bind=db.engine)()


   
#Página que lista as transações
@transaction_bp.route('/transactions')
@login_required
def transactions():
    """
    Esta função lida com a exibição de transações para o usuário conectado.

    Parâmetros:
    Nenhum

    Retorna:
    render_template: Um modelo HTML renderizado com transações e informações de paginação.
    """
    # Cria uma nova sessão de banco de dados
    session = create_session()

    try:
        user_id = current_user.user_id  

        # Captura o número da página atual da query string, padrão é 1
        page = request.args.get('page', 1, type=int)
        per_page = 10  # Número de transações por página

        # Cria a consulta base
        query = session.query(Transaction).options(
            joinedload(Transaction.payment_wallet),
            joinedload(Transaction.receiving_wallet),
            joinedload(Transaction.crypto_payment),
            joinedload(Transaction.crypto_receive),
            joinedload(Transaction.crypto_fee)
        ).join(
            Transaction.receiving_wallet
        ).filter(
            Wallet.wallet_user_id == user_id
        ).order_by(
            Transaction.transaction_date.desc(),
            Transaction.transactions_id.desc()
        )

        # Total de transações antes da paginação
        total_transactions = query.count()

        # Aplica a paginação
        cons_transactions = query.limit(per_page).offset((page - 1) * per_page).all()

        # Calcula o total de páginas
        total_pages = ceil(total_transactions / per_page)

    finally:
        # Garante que a sessão seja fechada corretamente
        session.close()

    # Renderiza o template com as transações e informações de paginação
    return render_template(
        'operacoes/transactions.html', 
        cons_transactions=cons_transactions,
        current_page=page,
        total_pages=total_pages
    )


#Pega preço atual da morda para preencher campos tela transsação
@transaction_bp.route('/get_price/<int:cryptocurrency_id>', methods=['GET'])#-
def get_price(cryptocurrency_id):
    """
    Esta função recupera o preço mais recente de uma criptomoeda específica.

    if latest_price:
        return jsonify({'price': latest_price[0]})
    Parâmetros:
    id_criptomoeda (int): O identificador exclusivo da criptomoeda.
    
    Retorna:
    JSON: Um objeto JSON contendo o preço mais recente da criptomoeda. Se não for encontrado nenhum preço, retorna 0.
    """
    session = create_session()    
    # Busca o preço mais recente da crypto selecionada
    latest_price = session.query(Price.price).filter(Price.price_crypto_id == cryptocurrency_id).order_by(Price.price_consult_datetime.desc()).first()

    if latest_price:
        return jsonify({'price': latest_price[0]})
    else:
        return jsonify({'price': 0})


    

#Fromulário de adicionar transação
@transaction_bp.route('/add_transactions')
@login_required
def add_transactions(): 
    """
    Esta função renderiza o modelo HTML para adicionar transações.
    Ela recupera dados do banco de dados e preenche o formulário com esses dados.
    Se houver dados de formulário armazenados na sessão, ele preenche o formulário com esses dados armazenados.

    Parâmetros:
    Nenhum

    Retorna:
    render_template: Um modelo HTML renderizado com os dados necessários para adicionar transações.
    """
    formTransactions = TransactionsForm()
    formAddWallet = AddWalletForm()
    formAddCrypto = AddCryptoForm()
    db_session = create_session()  # Renomeado para evitar conflito com flask.session

    try:        
        # Busca as informações no banco
        transactions = db_session.query(Transaction).all()
        wallets = db_session.query(Wallet).filter(
            Wallet.wallet_status=='N',
            Wallet.wallet_user_id == current_user.user_id
        ).all()
        cryptos = db_session.query(Cryptocurrency).filter(Cryptocurrency.crypto_status=='N').order_by(Cryptocurrency.crypto_symbol).all()

        # Preencher as informações do banco no HTML
        formTransactions.crypto_payment.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_symbol} - ({crypto.crypto_name})") for crypto in cryptos]

        formTransactions.crypto_fee.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_symbol} - ({crypto.crypto_name})") for crypto in cryptos]

        formTransactions.crypto_receive.choices = [('', '')] + [(crypto.crypto_id, f"{crypto.crypto_symbol} - ({crypto.crypto_name})") for crypto in cryptos]

        formTransactions.payment_wallet.choices = [('', '')] + [(wallet.wallet_id, wallet.wallet_name) for wallet in wallets]

        formTransactions.receiving_wallet.choices = [('', '')] + [(wallet.wallet_id, wallet.wallet_name) for wallet in wallets]

        # Verificar se existem dados armazenados na sessão para recuperar preenchimento
        if 'form_data' in session:
            form_data = session.pop('form_data') 

            # Preencher o formulário com os dados recuperados
            formTransactions.transaction_type.data = form_data.get('transaction_type')
            formTransactions.transaction_date.data = form_data.get('transaction_date')
            formTransactions.receiving_wallet.data = form_data.get('receiving_wallet_id')
            formTransactions.payment_wallet.data = form_data.get('payment_wallet_id')
            formTransactions.crypto_payment.data = form_data.get('crypto_payment_id')
            formTransactions.crypto_payment_price.data = form_data.get('crypto_payment_price')
            formTransactions.crypto_payment_quantity.data = form_data.get('crypto_payment_quantity')
            formTransactions.total_paid.data = form_data.get('total_paid')
            formTransactions.crypto_receive.data = form_data.get('crypto_receive_id')
            formTransactions.crypto_receive_price.data = form_data.get('crypto_receive_price')
            formTransactions.crypto_receive_quantity.data = form_data.get('crypto_receive_quantity')
            formTransactions.total_received.data = form_data.get('total_received')
            formTransactions.crypto_fee.data = form_data.get('crypto_fee_id')
            formTransactions.crypto_fee_price.data = form_data.get('crypto_fee_price')
            formTransactions.crypto_fee_quantity.data = form_data.get('crypto_fee_quantity')
            formTransactions.total_fee.data = form_data.get('total_fee')

    finally:
        db_session.close() 

    return render_template('operacoes/add_transactions.html', transactions=transactions, wallets=wallets, cryptos=cryptos, formTransactions=formTransactions, formAddWallet=formAddWallet, formAddCrypto=formAddCrypto)




# Função normalize_decimal (exemplo)
def normalize_decimal(value):
    """
    Função para substituir vírgulas por pontos em valores numéricos.

    Parâmetros:
    value (str, int, float): O valor a ser normalizado.

    Retorna:
    str: O valor normalizado. Se a entrada for uma string, substitui as vírgulas por pontos.
         Se a entrada for um inteiro ou float, converte o número em uma string.
         Levanta um ValueError se a entrada for de um tipo inesperado.
    """
    if isinstance(value, str):
        return value.replace(',', '.')
    elif isinstance(value, (int, float)):
        return str(value)  # Converte números diretamente em string
    else:
        raise ValueError(f"Tipo de valor inesperado: {type(value)}")

    

#função chamada no formulário de adicionar transação para inserir a transação no banco
@transaction_bp.route('/add_transaction', methods=['POST'])
def add_transaction():
    """
    Adiciona uma nova transação de criptomoedas.

    Esta função processa os dados da transação enviados via formulário e realiza a operação correspondente com base no tipo de transação 
    (compra, venda, saldo ou transferência). A função também normaliza e converte os valores monetários para o tipo float antes de 
    realizar as operações.

    A função segue os seguintes passos:
    1. Obtém os dados da transação do formulário.
    2. Normaliza e converte os valores de preço e quantidade para float.
    3. Cria uma sessão para interagir com o banco de dados.
    4. Chama a função apropriada para realizar a operação com base no tipo de transação.
    5. Em caso de erro, reverte as alterações na sessão e exibe uma mensagem de erro.

    Parâmetros:
    Nenhum. A função obtém os dados diretamente do formulário da requisição.

    Retorna:
    redirect: Redireciona para a página de adição de transações após a tentativa de adicionar a transação.

    Exceções:
    Levanta uma exceção em caso de erro durante o processo de adição da transação e reverte as alterações na sessão do banco de dados.
    """
    
    session = None
    
    try:
        # Dados gerais da transação
        transaction_type = request.form.get('transaction_type')
        transaction_date = request.form.get('transaction_date')
        
        # Dados carteiras da transação        
        receiving_wallet_id = request.form.get('receiving_wallet')
        payment_wallet_id = request.form.get('payment_wallet')
        
        # Dados das moedas pagadoras
        crypto_payment_id = request.form.get('crypto_payment')
        crypto_payment_price = request.form.get('crypto_payment_price')
        crypto_payment_quantity = request.form.get('crypto_payment_quantity')
        total_paid = request.form.get('total_paid')
        
        # Normalizando e convertendo para float
        crypto_payment_price = float(normalize_decimal(crypto_payment_price)) if crypto_payment_price else 0.0
        crypto_payment_quantity = float(normalize_decimal(crypto_payment_quantity)) if crypto_payment_quantity else 0.0
        total_paid = float(normalize_decimal(total_paid)) if total_paid else 0.0
        
        # Dados da moeda recebedora
        crypto_receive_id = request.form.get('crypto_receive')
        crypto_receive_price = request.form.get('crypto_receive_price')
        crypto_receive_quantity = request.form.get('crypto_receive_quantity')
        total_received = request.form.get('total_received')
        
        # Normalizando e convertendo para float
        crypto_receive_price = float(normalize_decimal(crypto_receive_price)) if crypto_receive_price else 0.0
        crypto_receive_quantity = float(normalize_decimal(crypto_receive_quantity)) if crypto_receive_quantity else 0.0
        total_received = float(normalize_decimal(total_received)) if total_received else 0.0


        # Dados da taxa
        crypto_fee_id = request.form.get('crypto_fee')
        crypto_fee_price = request.form.get('crypto_fee_price')
        crypto_fee_quantity = request.form.get('crypto_fee_quantity')
        total_fee = request.form.get('total_fee')
        
        # Normalizando e convertendo para float
        crypto_fee_price = float(normalize_decimal(crypto_fee_price)) if crypto_fee_price else 0.0
        crypto_fee_quantity = float(normalize_decimal(crypto_fee_quantity)) if crypto_fee_quantity else 0.0
        total_fee = float(normalize_decimal(total_fee)) if total_fee else 0.0                         

        # Cria a sessão
        session = create_session()

        # Realizar operações baseadas no tipo de transação
        if transaction_type == 'Compra':
            realizar_compra(session, transaction_date, payment_wallet_id, receiving_wallet_id,crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid,crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee,transaction_type='Compra')
        elif transaction_type == 'Saldo':
            enter_balance(session, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date)
        elif transaction_type == 'Venda':
            realizar_venda(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type='Venda')
        elif transaction_type == 'Transferência':
            realizar_transferencia(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type='Transferência')
                

    except Exception as e:
        if session is not None:
            session.rollback()
        flash(f'Erro ao tentar adicionar transação: {e}', 'alert-danger')
    
    return redirect(url_for('transaction.add_transactions'))

    

#********     COMPRA    *******     COMPRA    ********
#armazenar dados do formulário de transações para qualquer transação
def store_data(transaction_type, receiving_wallet_id=None, payment_wallet_id=None,
               crypto_receive_id=None, crypto_receive_price=None, crypto_receive_quantity=None,
               total_received=None, crypto_payment_id=None, crypto_payment_price=None,
               crypto_payment_quantity=None, total_paid=None, crypto_fee_id=None,
               crypto_fee_price=None, crypto_fee_quantity=None, total_fee=None, transaction_date=None):
    """
    Armazena dados de transação na sessão.

    Parâmetros:
    transaction_type (str): O tipo de transação.
    receiving_wallet_id (int, opcional): O ID da carteira de recebimento. Padrão é None.
    payment_wallet_id (int, opcional): O ID da carteira de pagamento. Padrão é None.
    crypto_receive_id (int, opcional): O ID da criptomoeda recebida. Padrão é None.
    crypto_receive_price (float, opcional): O preço da criptomoeda recebida. Padrão é None.
    crypto_receive_quantity (float, opcional): A quantidade da criptomoeda recebida. Padrão é None.
    total_received (float, opcional): O total recebido. Padrão é None.
    crypto_payment_id (int, opcional): O ID da criptomoeda paga. Padrão é None.
    crypto_payment_price (float, opcional): O preço da criptomoeda paga. Padrão é None.
    crypto_payment_quantity (float, opcional): A quantidade da criptomoeda paga. Padrão é None.
    total_paid (float, opcional): O total pago. Padrão é None.
    crypto_fee_id (int, opcional): O ID da criptomoeda de taxa. Padrão é None.
    crypto_fee_price (float, opcional): O preço da criptomoeda de taxa. Padrão é None.
    crypto_fee_quantity (float, opcional): A quantidade da criptomoeda de taxa. Padrão é None.
    total_fee (float, opcional): O total da taxa. Padrão é None.
    transaction_date (str, opcional): A data da transação. Padrão é None.

    Retorna:
    None
    """
    session['form_data'] = {
        'transaction_type': transaction_type,
        'transaction_date': transaction_date,
        'payment_wallet_id': payment_wallet_id,
        'receiving_wallet_id': receiving_wallet_id,
        'crypto_payment_id': crypto_payment_id,
        'crypto_payment_price': crypto_payment_price,
        'crypto_payment_quantity': crypto_payment_quantity,
        'total_paid': total_paid,
        'crypto_receive_id': crypto_receive_id,
        'crypto_receive_price': crypto_receive_price,
        'crypto_receive_quantity': crypto_receive_quantity,
        'total_received': total_received,
        'crypto_fee_id': crypto_fee_id,
        'crypto_fee_price': crypto_fee_price,
        'crypto_fee_quantity': crypto_fee_quantity,
        'total_fee': total_fee
    }



#esta função é usada na transação da compra e da venda
def check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date=None):
    """
    Esta função verifica se todos os campos obrigatórios estão preenchidos em uma transação de compra.
    Se algum campo estiver faltando, armazena os dados da transação na sessão e redireciona para a página de transação com uma mensagem de erro.

    Parâmetros:
    payment_wallet_id (int): O ID da carteira de pagamento.
    receiving_wallet_id (int): O ID da carteira de recebimento.
    crypto_payment_id (int): O ID da criptomoeda usada para pagamento.
    crypto_payment_price (float): O preço da criptomoeda usada para pagamento.
    crypto_payment_quantity (float): A quantidade da criptomoeda usada para pagamento.
    total_paid (float): O total pago.
    crypto_receive_id (int): O ID da criptomoeda a ser recebida.
    crypto_receive_price (float): O preço da criptomoeda a ser recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda a ser recebida.
    total_received (float): O total recebido.
    crypto_fee_id (int): O ID da criptomoeda usada para a taxa de transação.
    crypto_fee_price (float): O preço da criptomoeda usada para a taxa de transação.
    crypto_fee_quantity (float): A quantidade da criptomoeda usada para a taxa de transação.
    total_fee (float): A taxa total da transação.
    transaction_type (str): O tipo da transação.
    transaction_date (str, opcional): A data da transação. Padrão é None.

    Retorna:
    redirect: Se algum campo estiver faltando, redireciona para a página de transação com uma mensagem de erro.
    """
    if not all([payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type]):
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_payment_id=crypto_payment_id,
            crypto_payment_price=crypto_payment_price,
            crypto_payment_quantity=crypto_payment_quantity,
            total_paid=total_paid,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee,
            transaction_date=transaction_date
        )
        flash('Preencha/Verifique todos os campos!', 'alert-danger')
        return redirect(url_for('transaction.add_transactions'))

    if not transaction_date:
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_payment_id=crypto_payment_id,
            crypto_payment_price=crypto_payment_price,
            crypto_payment_quantity=crypto_payment_quantity,
            total_paid=total_paid,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee
        )
        flash('Preencha a data!', 'alert-danger')
        return redirect(url_for('transaction.add_transactions'))





def realizar_compra(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type):
    """
    Realiza uma compra de criptomoedas entre carteiras.

    Esta função verifica se todos os campos obrigatórios estão preenchidos e se há saldo suficiente nas carteiras para realizar a compra. 
    Se todas as condições forem atendidas, a transação é registrada no banco de dados e os saldos das carteiras são atualizados.
    Caso contrário, uma mensagem de erro é exibida e o usuário é redirecionado para a página de adição de transações.

    Parâmetros:
    session (Session): A sessão do banco de dados para realizar operações.
    transaction_date (str): A data da transação no formato 'YYYY-MM-DD'.
    payment_wallet_id (str): O ID da carteira de pagamento.
    receiving_wallet_id (str): O ID da carteira de recebimento.
    crypto_payment_id (str): O ID da criptomoeda utilizada para pagamento.
    crypto_payment_price (float): O preço da criptomoeda utilizada para pagamento.
    crypto_payment_quantity (float): A quantidade da criptomoeda a ser paga.
    total_paid (float): O total pago na transação.
    crypto_receive_id (str): O ID da criptomoeda a ser recebida.
    crypto_receive_price (float): O preço da criptomoeda a ser recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda a ser recebida.
    total_received (float): O total recebido na transação.
    crypto_fee_id (str): O ID da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_price (float): O preço da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_quantity (float): A quantidade da criptomoeda utilizada para pagamento da taxa.
    total_fee (float): O total da taxa da transação.
    transaction_type (str): O tipo da transação (por exemplo, "compra").

    Retorna:
    redirect: Redireciona para a página de adição de transações se houver saldo insuficiente ou se algum campo obrigatório não estiver preenchido.
    Caso contrário, não retorna nada.

    Exceções:
    Levanta uma exceção em caso de erro durante o processo de compra e reverte as alterações na sessão do banco de dados.
    """
    try:
        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date)
        if redirect_result_com:
            return redirect_result_com
        
        # Carteira de pagamento
        payment_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_payment_id).first()
        # Carteira de recebimento
        receiving_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

       
        # Consulta se tem saldo suficiente para a taxa na carteira da transação
        fee_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_fee_id
        ).first()

        # Consulta saldo da moeda pagadora na carteira da transação
        crypto_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_payment_id
        ).first()
        
        saldo_pagto_tran = False

        if crypto_payment_id != crypto_fee_id:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (fee_wallet_balance.balance >= crypto_fee_quantity) and (crypto_wallet_balance.balance >= crypto_payment_quantity)
        else:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (crypto_wallet_balance.balance >= (crypto_fee_quantity + crypto_payment_quantity))

        # Verifica se tem saldo da crypto da taxa
        if saldo_pagto_tran:
           
            # Criar a transação
            transaction = Transaction(
                transaction_type=transaction_type, 
                transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'), 
                payment_wallet_id=payment_wallet_id, 
                receiving_wallet_id=receiving_wallet_id, 
                crypto_payment_id=crypto_payment_id, 
                crypto_payment_price=crypto_payment_price, 
                crypto_payment_quantity=crypto_payment_quantity, 
                total_paid=total_paid, 
                crypto_receive_id=crypto_receive_id, 
                crypto_receive_price=crypto_receive_price, 
                crypto_receive_quantity=crypto_receive_quantity, 
                total_received=total_received, 
                crypto_fee_id=crypto_fee_id, 
                crypto_fee_price=crypto_fee_price, 
                crypto_fee_quantity=crypto_fee_quantity, 
                total_fee=total_fee
            )
            
            # Registrar a transação
            session.add(transaction)

            # Atualizar saldo das carteiras
            if fee_wallet_balance:
                fee_wallet_balance.balance -= crypto_fee_quantity

            if crypto_wallet_balance:
                crypto_wallet_balance.balance -= crypto_payment_quantity

            if receiving_wallet: # carteira de recebimento existe
                receiving_wallet.balance += crypto_receive_quantity
            else:
                # Se a crypto não existe em balance, insere
                novo_saldo = WalletBalance(
                    balance_wallet_id=receiving_wallet_id,
                    balance_crypto_id=crypto_receive_id,
                    balance=crypto_receive_quantity
                )
                session.add(novo_saldo)
            
            session.commit()

            flash('Transação realizada com sucesso!', 'alert-success')
        else:
            store_data(
                transaction_type=transaction_type,
                payment_wallet_id=payment_wallet_id,
                receiving_wallet_id=receiving_wallet_id,
                crypto_payment_id=crypto_payment_id,
                crypto_payment_price=crypto_payment_price,
                crypto_payment_quantity=crypto_payment_quantity,
                total_paid=total_paid,
                crypto_receive_id=crypto_receive_id,
                crypto_receive_price=crypto_receive_price,
                crypto_receive_quantity=crypto_receive_quantity,
                total_received=total_received,
                crypto_fee_id=crypto_fee_id,
                crypto_fee_price=crypto_fee_price,
                crypto_fee_quantity=crypto_fee_quantity,
                total_fee=total_fee,
                transaction_date=transaction_date
            )
            flash('Saldo Insuficiente', 'alert-danger')
            return redirect(url_for('transaction.add_transactions'))
    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        raise


#********     SALDO    *******     SALDO    ********
#verifica campos obrigatórios
def check_mandatory_fields_in_balance(receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date=None):
    """
    Esta função verifica se todos os campos obrigatórios para uma transação de saldo estão preenchidos.

    Parâmetros:
    receiving_wallet_id (int): O ID da carteira recebendo.
    crypto_receive_id (int): O ID da criptomoeda a ser recebida.
    crypto_receive_price (float): O preço da criptomoeda a ser recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda a ser recebida.
    total_received (float): O total recebido.
    transaction_date (str, opcional): A data da transação. Padrão é None.

    Retorna:
    Se algum campo obrigatório estiver faltando ou a data da transação não for fornecida, redireciona para a página 'add_transactions' com uma mensagem de aviso.
    Se todos os campos obrigatórios estiverem preenchidos e a data da transação for fornecida, retorna None.
    """
    if not all([receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received]):
        store_data(
            transaction_type='Saldo',
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            transaction_date=transaction_date
        )
        flash('Preencha/Verifique todos os campos!', 'alert-danger')
        return redirect(url_for('transaction.add_transactions'))

    if not transaction_date:
        store_data(
            transaction_type='Saldo',
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received
        )
        flash('Preencha a data!', 'alert-danger')
        return redirect(url_for('transaction.add_transactions'))


    

def enter_balance(db_session, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date):
    """
    Esta função é usada para adicionar um saldo a uma carteira específica para uma criptomoeda específica.
    Ela cria um registro de transação e atualiza o saldo da carteira.

    Parâmetros:
    db_session (Sessão SQLAlchemy): O objeto de sessão do banco de dados.
    receiving_wallet_id (int): O ID da carteira que receberá o saldo.
    crypto_receive_id (int): O ID da criptomoeda que será recebida.
    crypto_receive_price (float): O preço da criptomoeda que será recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda que será recebida.
    total_received (float): O valor total recebido na transação.
    transaction_date (str): A data da transação no formato 'YYYY-MM-DD'.

    Retorna:
    None
    """
    try:
        # Verificar campos obrigatórios
        redirect_result = check_mandatory_fields_in_balance(receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, transaction_date)
        if redirect_result:
            return redirect_result

        # Obter o saldo atual da carteira para a criptomoeda específica
        balance_wallet = db_session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

        # Criar um registro de transação
        transaction = Transaction(
            transaction_type='Saldo',
            transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'),
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received
        )

        db_session.add(transaction)
        db_session.commit()

        # Atualizar o saldo da carteira
        if balance_wallet:
            balance_wallet.balance += crypto_receive_quantity
        else:
            novo_saldo = WalletBalance(
                balance_wallet_id=receiving_wallet_id,
                balance_crypto_id=crypto_receive_id,
                balance=crypto_receive_quantity
            )
            db_session.add(novo_saldo)

        db_session.commit()

        flash('Saldo adicionado com sucesso!', 'alert-success')
    except Exception as e:
        db_session.rollback()
        flash(f'Erro na Transação de Compra: {e}', 'alert-danger')
        raise




#************************************************************************************************
def realizar_venda(session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type):
    """
    Realiza uma venda de criptomoedas entre carteiras.

    Esta função verifica se todos os campos obrigatórios estão preenchidos e se há saldo suficiente nas carteiras para realizar a venda. 
    Se todas as condições forem atendidas, a transação é registrada no banco de dados e os saldos das carteiras são atualizados.
    Caso contrário, uma mensagem de erro é exibida e o usuário é redirecionado para a página de adição de transações.

    Parâmetros:
    session (Session): A sessão do banco de dados para realizar operações.
    transaction_date (str): A data da transação no formato 'YYYY-MM-DD'.
    payment_wallet_id (str): O ID da carteira de pagamento.
    receiving_wallet_id (str): O ID da carteira de recebimento.
    crypto_payment_id (str): O ID da criptomoeda utilizada para pagamento.
    crypto_payment_price (float): O preço da criptomoeda utilizada para pagamento.
    crypto_payment_quantity (float): A quantidade da criptomoeda a ser paga.
    total_paid (float): O total pago na transação.
    crypto_receive_id (str): O ID da criptomoeda a ser recebida.
    crypto_receive_price (float): O preço da criptomoeda a ser recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda a ser recebida.
    total_received (float): O total recebido na transação.
    crypto_fee_id (str): O ID da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_price (float): O preço da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_quantity (float): A quantidade da criptomoeda utilizada para pagamento da taxa.
    total_fee (float): O total da taxa da transação.
    transaction_type (str): O tipo da transação (por exemplo, "venda").

    Retorna:
    redirect: Redireciona para a página de adição de transações se houver saldo insuficiente ou se algum campo obrigatório não estiver preenchido.
    Caso contrário, não retorna nada.

    Exceções:
    Levanta uma exceção em caso de erro durante o processo de venda e reverte as alterações na sessão do banco de dados.
    """
    try:
        
        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_purchase(payment_wallet_id, receiving_wallet_id, crypto_payment_id, crypto_payment_price, crypto_payment_quantity, total_paid, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date)
        if redirect_result_com:
            return redirect_result_com
        
        # Carteira de pagamento
        payment_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_payment_id).first()
        # Carteira de recebimento
        receiving_wallet = session.query(WalletBalance).filter_by(balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id).first()

        # Consulta se tem saldo suficiente para a taxa na carteira da transação
        fee_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_fee_id
        ).first()

        # Consulta saldo da moeda pagadora na carteira da transação
        crypto_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, 
            balance_crypto_id=crypto_payment_id
        ).first()

        saldo_pagto_tran = False

        if crypto_payment_id != crypto_fee_id:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (fee_wallet_balance.balance >= crypto_fee_quantity) and (crypto_wallet_balance.balance >= crypto_payment_quantity)
        else:
            if fee_wallet_balance and crypto_wallet_balance:
                saldo_pagto_tran = (crypto_wallet_balance.balance >= (crypto_fee_quantity + crypto_payment_quantity))

        # Verifica se tem saldo da crypto da taxa
        if saldo_pagto_tran:
            
            # Criar a transação
            transaction = Transaction(
                transaction_type=transaction_type, 
                transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'), 
                payment_wallet_id=payment_wallet_id, 
                receiving_wallet_id=receiving_wallet_id, 
                crypto_payment_id=crypto_payment_id, 
                crypto_payment_price=crypto_payment_price, 
                crypto_payment_quantity=crypto_payment_quantity, 
                total_paid=total_paid, 
                crypto_receive_id=crypto_receive_id, 
                crypto_receive_price=crypto_receive_price, 
                crypto_receive_quantity=crypto_receive_quantity, 
                total_received=total_received, 
                crypto_fee_id=crypto_fee_id, 
                crypto_fee_price=crypto_fee_price, 
                crypto_fee_quantity=crypto_fee_quantity, 
                total_fee=total_fee
            )
            
            # Registrar a transação
            session.add(transaction)
            session.commit()

            if fee_wallet_balance: # tem saldo para taxa
                fee_wallet_balance.balance -= crypto_fee_quantity

            if crypto_wallet_balance: # tem saldo para pagamento
                crypto_wallet_balance.balance -= crypto_payment_quantity

            if receiving_wallet: # carteira de recebimento existe
                receiving_wallet.balance += crypto_receive_quantity
            else:
                # Se a crypto não existe em balance, insere
                novo_saldo = WalletBalance(
                    balance_wallet_id=receiving_wallet_id,
                    balance_crypto_id=crypto_receive_id,
                    balance=crypto_receive_quantity
                )
                session.add(novo_saldo)
            
            session.commit()

            flash('Transação realizada com sucesso!', 'alert-success')
        else:
            store_data(
                transaction_type=transaction_type,
                payment_wallet_id=payment_wallet_id,
                receiving_wallet_id=receiving_wallet_id,
                crypto_payment_id=crypto_payment_id,
                crypto_payment_price=crypto_payment_price,
                crypto_payment_quantity=crypto_payment_quantity,
                total_paid=total_paid,
                crypto_receive_id=crypto_receive_id,
                crypto_receive_price=crypto_receive_price,
                crypto_receive_quantity=crypto_receive_quantity,
                total_received=total_received,
                crypto_fee_id=crypto_fee_id,
                crypto_fee_price=crypto_fee_price,
                crypto_fee_quantity=crypto_fee_quantity,
                total_fee=total_fee,
                transaction_date=transaction_date
            )
            flash('Saldo Insuficiente!', 'alert-danger')
            return redirect(url_for('transaction.add_transactions'))
                        
    except Exception as e:
        session.rollback()
        flash(f'Erro na Transação de Venda: {e}', 'alert-danger')
        raise
    

#************* REALIZANDO TRANSFERÊNCIA *******************
def check_mandatory_fields_in_transf(
    payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,
    crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date=None
    ):
    """
    Verifica se todos os campos obrigatórios para a transferência estão preenchidos.

    Esta função valida a presença de todos os campos necessários para realizar uma transferência de criptomoedas. Se algum campo obrigatório
    não estiver preenchido, os dados da transação são armazenados e uma mensagem de erro é exibida. A função redireciona o usuário para a
    página de adição de transações.

    Parâmetros:
    payment_wallet_id (str): O ID da carteira de pagamento.
    receiving_wallet_id (str): O ID da carteira de recebimento.
    crypto_receive_id (str): O ID da criptomoeda a ser recebida.
    crypto_receive_price (float): O preço da criptomoeda a ser recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda a ser recebida.
    total_received (float): O total recebido na transação.
    crypto_fee_id (str): O ID da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_price (float): O preço da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_quantity (float): A quantidade da criptomoeda utilizada para pagamento da taxa.
    total_fee (float): O total da taxa da transação.
    transaction_type (str): O tipo da transação (por exemplo, "transferência").
    transaction_date (str, opcional): A data da transação no formato 'YYYY-MM-DD'. O padrão é None.

    Retorna:
    redirect: Redireciona para a página de adição de transações se algum campo obrigatório não estiver preenchido ou se a data não estiver
              informada. Caso contrário, não retorna nada.

    Exceções:
    Não levanta exceções, mas exibe mensagens de erro ao usuário se os campos obrigatórios não forem preenchidos.
    """
    # Verificar se todos os campos obrigatórios estão preenchidos
    if not all([
        payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,
        crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type
    ]):
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee,
            transaction_date=transaction_date
        )
        flash('Preencha/Verifique todos os campos!', 'alert-danger')
        return redirect(url_for('transaction.add_transactions'))

    if not transaction_date:
        store_data(
            transaction_type=transaction_type,
            payment_wallet_id=payment_wallet_id,
            receiving_wallet_id=receiving_wallet_id,
            crypto_receive_id=crypto_receive_id,
            crypto_receive_price=crypto_receive_price,
            crypto_receive_quantity=crypto_receive_quantity,
            total_received=total_received,
            crypto_fee_id=crypto_fee_id,
            crypto_fee_price=crypto_fee_price,
            crypto_fee_quantity=crypto_fee_quantity,
            total_fee=total_fee
        )
        flash('Preencha a data!', 'alert-danger')
        return redirect(url_for('transaction.add_transactions'))


def realizar_transferencia(
    session, transaction_date, payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity,
    total_received, crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type
    ):
    """
    Realiza uma transferência de criptomoedas entre carteiras.

    Esta função verifica se as carteiras de pagamento e recebimento existem, se há saldo suficiente para a transferência e para a taxa
    associada. Se todas as condições forem atendidas, a transação é registrada no banco de dados e os saldos das carteiras são atualizados.
    Caso contrário, uma mensagem de erro é exibida e as alterações são revertidas.

    Parâmetros:
    session (Session): A sessão do banco de dados para realizar operações.
    transaction_date (str): A data da transação no formato 'YYYY-MM-DD'.
    payment_wallet_id (str): O ID da carteira de pagamento.
    receiving_wallet_id (str): O ID da carteira de recebimento.
    crypto_receive_id (str): O ID da criptomoeda a ser recebida.
    crypto_receive_price (float): O preço da criptomoeda a ser recebida.
    crypto_receive_quantity (float): A quantidade da criptomoeda a ser recebida.
    total_received (float): O total recebido na transação.
    crypto_fee_id (str): O ID da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_price (float): O preço da criptomoeda utilizada para pagamento da taxa.
    crypto_fee_quantity (float): A quantidade da criptomoeda utilizada para pagamento da taxa.
    total_fee (float): O total da taxa da transação.
    transaction_type (str): O tipo da transação (por exemplo, "transferência").

    Retorna:
    None: Se a transferência for realizada com sucesso, uma mensagem de sucesso é exibida. 
          Se houver erro ou saldo insuficiente, uma mensagem de erro é exibida.

    Exceções:
    Levanta uma exceção em caso de erro durante o processo de transferência.
    """
    try:
        # Verificar campos obrigatórios
        redirect_result_com = check_mandatory_fields_in_transf(
            payment_wallet_id, receiving_wallet_id, crypto_receive_id, crypto_receive_price, crypto_receive_quantity, total_received,
            crypto_fee_id, crypto_fee_price, crypto_fee_quantity, total_fee, transaction_type, transaction_date
        )
        if redirect_result_com:
            return redirect_result_com
        
        # Verifica o saldo da carteira de pagamento para a criptomoeda de pagamento e a taxa
        payment_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_receive_id
        ).first()
        
        fee_wallet_balance = session.query(WalletBalance).filter_by(
            balance_wallet_id=payment_wallet_id, balance_crypto_id=crypto_fee_id
        ).first()

        # Verifica se as carteiras foram encontradas
        if not payment_wallet_balance:
            flash(f'Carteira de pagamento não encontrada para a criptomoeda de recebimento.', 'alert-danger')
            return
        if not fee_wallet_balance:
            flash(f'Carteira de pagamento não encontrada para a criptomoeda da taxa.', 'alert-danger')
            return

        saldo_transferencia = False
        print(f"Payment Wallet Balance: {payment_wallet_balance.balance}")
        print(f"Fee Wallet Balance: {fee_wallet_balance.balance}")
        print(f"Crypto Receive Quantity: {crypto_receive_quantity}")
        print(f"Crypto Fee Quantity: {crypto_fee_quantity}")
       
        # Verificar se há saldo suficiente para a taxa e a quantidade a ser transferida
        if crypto_receive_id == crypto_fee_id:
            # Verifica se a soma das duas quantidades cabe no saldo da carteira de pagamento
            if payment_wallet_balance.balance >= (crypto_receive_quantity + crypto_fee_quantity):
                saldo_transferencia = True
                payment_wallet_balance.balance -= (crypto_receive_quantity + crypto_fee_quantity)
        else:
            # Verifica se o saldo de ambas as carteiras é suficiente
            if (float(payment_wallet_balance.balance) >= float(crypto_receive_quantity)) and (float(fee_wallet_balance.balance) >= float(crypto_fee_quantity)):
                saldo_transferencia = True
                payment_wallet_balance.balance -= crypto_receive_quantity
                fee_wallet_balance.balance -= crypto_fee_quantity

        if saldo_transferencia:
            # Cria a transação
            transaction = Transaction(
                transaction_type=transaction_type, 
                transaction_date=datetime.strptime(transaction_date, '%Y-%m-%d'), 
                payment_wallet_id=payment_wallet_id, 
                receiving_wallet_id=receiving_wallet_id,
                crypto_payment_id=crypto_receive_id, 
                crypto_payment_price=crypto_receive_price, 
                crypto_payment_quantity=crypto_receive_quantity, 
                crypto_receive_id=crypto_receive_id, 
                crypto_receive_price=crypto_receive_price, 
                crypto_receive_quantity=crypto_receive_quantity, 
                total_received=total_received, 
                crypto_fee_id=crypto_fee_id, 
                crypto_fee_price=crypto_fee_price, 
                crypto_fee_quantity=crypto_fee_quantity, 
                total_fee=total_fee
            )
            
            # Registra a transação
            session.add(transaction)
            
            # Atualiza a carteira de recebimento
            wallet_balance_receb = session.query(WalletBalance).filter_by(
                balance_wallet_id=receiving_wallet_id, balance_crypto_id=crypto_receive_id
            ).first()
            if wallet_balance_receb:
                wallet_balance_receb.balance += crypto_receive_quantity
            else:
                novo_recebimento_trans = WalletBalance(
                    balance_wallet_id=receiving_wallet_id,
                    balance_crypto_id=crypto_receive_id,
                    balance=crypto_receive_quantity
                )
                session.add(novo_recebimento_trans)

            # Commit das mudanças
            session.commit()
            flash('Transação realizada com sucesso!', 'alert-success')        
        else:
            store_data(
                transaction_type=transaction_type,
                payment_wallet_id=payment_wallet_id,
                receiving_wallet_id=receiving_wallet_id,
                crypto_receive_id=crypto_receive_id,
                crypto_receive_price=crypto_receive_price,
                crypto_receive_quantity=crypto_receive_quantity,
                total_received=total_received,
                crypto_fee_id=crypto_fee_id,
                crypto_fee_price=crypto_fee_price,
                crypto_fee_quantity=crypto_fee_quantity,
                total_fee=total_fee,
                transaction_date=transaction_date
            )
            flash(f'Saldo Insuficiente! Saldo taxa: {fee_wallet_balance.balance}, Saldo Moeda Transferência {payment_wallet_balance.balance}', 'alert-danger')
            session.rollback()            
    except Exception as e:
        flash(f'Erro ao realizar transferência: {e}', 'alert-danger')
        session.rollback()
        raise



# **********   DELETE TRANSACTION *******  DELETE   ************************************************
@transaction_bp.route('/transaction.delete_transaction', methods=['POST'])
@login_required
def delete_transaction():
    """
    Exclui uma transação do banco de dados e atualiza os saldos das carteiras.

    Parâmetros:
    session (sqlalchemy.orm.Session): A sessão do banco de dados.

    Retorna:
    redirect: Redireciona para a página de transações após excluir a transação.
    """
    session = create_session()

    try:
        transacao_id = request.form.get('transactions_id')

        if transacao_id:

            transaction = session.query(Transaction).filter_by(transactions_id=transacao_id).first()

            if transaction:
                tipo_transacao = transaction.transaction_type
                wallet_id_saida = transaction.payment_wallet_id
                wallet_id_recebimento = transaction.receiving_wallet_id
                crypto_payment_id = transaction.crypto_payment_id
                crypto_fee_id = transaction.crypto_fee_id
                crypto_receive_id = transaction.crypto_receive_id
                crypto_payment_quantity = transaction.crypto_payment_quantity
                crypto_fee_quantity = transaction.crypto_fee_quantity
                crypto_receive_quantity = transaction.crypto_receive_quantity

                balance = True

                # Busca os saldos
                wallet_balance_payment = session.query(WalletBalance).filter_by(balance_wallet_id=wallet_id_saida, balance_crypto_id=crypto_payment_id).first()

                wallet_balance_fee = session.query(WalletBalance).filter_by(balance_wallet_id=wallet_id_saida, balance_crypto_id=crypto_fee_id).first()

                wallet_balance_receive = session.query(WalletBalance).filter_by(balance_wallet_id=wallet_id_recebimento, balance_crypto_id=crypto_receive_id).first()    

                if wallet_balance_receive:
                    if wallet_balance_receive.balance >= crypto_receive_quantity:
                        wallet_balance_receive.balance -= crypto_receive_quantity
                        session.add(wallet_balance_receive)

                        if wallet_balance_payment:
                            wallet_balance_payment.balance += crypto_payment_quantity
                            session.add(wallet_balance_payment)

                        if wallet_balance_fee:
                            wallet_balance_fee.balance += crypto_fee_quantity
                            if tipo_transacao == 'Transferência':
                                wallet_balance_fee.balance += crypto_receive_quantity
                                session.add(wallet_balance_fee)
                                session.add(wallet_balance_fee)                        

                        #session.add(wallet_balance_receive)                        
                    else:
                        balance = False
                        flash('Saldo insuficiente para excluir recebimento.', 'alert-danger')

                    if balance:
                        # Exclui a transação
                        session.delete(transaction)
                        session.commit()
                        flash(f'Transação excluída com sucesso.', 'alert-success')
                    else:
                        flash(f'Transação não tem saldo suficiente para ser excluída.', 'alert-danger')
        else:
            flash("Transação não encontrada.", 'alert-danger')

    except Exception as e:
        flash(f'Erro ao tentar excluir transação: {e}', 'alert-danger')
        if session:
            session.rollback()

    finally:
        session.close()

    return redirect(url_for('transaction.transactions'))




# ******    Implementar função de editar transação ********************************
