from flask import Blueprint, render_template, url_for, flash, request, redirect
from sqlalchemy import or_
from criptoControl.forms import AddWalletForm, AddCryptoForm
from criptoControl.models import db, Wallet, Cryptocurrency, Transaction
from flask_login import current_user, login_required
import logging

crypto_wallet_bp = Blueprint('crypto_wallet', __name__)

logging.basicConfig(level=logging.DEBUG)

#----------------  Adicionar Carteira  ---------------------------
@crypto_wallet_bp.route('/add_wallet', methods=['GET', 'POST'])
@login_required
def add_wallet():
    """
    Esta função lida com a adição de uma nova carteira de criptomoedas. Primeiro, valida os dados do formulário,
    verifica se a carteira já existe para o usuário atual e, em seguida, adiciona a nova carteira ao banco de dados.

    Parâmetros:
    - formAddWallet: Uma instância da classe AddWalletForm, que contém os dados do formulário para adicionar uma carteira.

    Retorna:
    - Se os dados do formulário são válidos e a carteira não existe, uma nova carteira é adicionada ao banco de dados,
      uma mensagem de flash de sucesso é exibida e o usuário é redirecionado para a página de carteiras.
    - Se os dados do formulário são inválidos ou a carteira já existe, uma mensagem de flash de erro é exibida.
    - Se ocorre uma exceção durante as operações de banco de dados, uma reversão é executada e uma mensagem de flash de erro é exibida.
    """
    formAddWallet = AddWalletForm()  # Criação do formulário
    if formAddWallet.validate_on_submit():
        wallet_name = formAddWallet.wallet_name.data.strip().upper()
        wallet_network = formAddWallet.wallet_network.data.strip().upper()

        try:
            # Verificar se a carteira já existe para o usuário atual
            existing_wallet = Wallet.query.filter_by(wallet_user_id=current_user.user_id, wallet_name=wallet_name).first()
            if existing_wallet:
                flash(f'A Carteira {wallet_name} já está cadastrada.', 'alert-warning')
                return redirect(url_for('views.wallets'))

            # Criar e adicionar a nova carteira
            wallet = Wallet(wallet_user_id=current_user.user_id, wallet_name=wallet_name, wallet_network=wallet_network)
            db.session.add(wallet)
            db.session.commit()
            flash(f'A Carteira {wallet_name} foi adicionada com sucesso', 'alert-success')
            return redirect(url_for('views.wallets'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar adicionar a carteira: {e}', 'alert-danger')

    return render_template('operacoes/add_wallet.html', formAddWallet=formAddWallet)


#------------------- Remover Carteira ------------------------
@crypto_wallet_bp.route('/delete_wallet', methods=['POST'])
@login_required
def delete_wallet():
    """
    Esta função lida com a exclusão de uma carteira de criptomoedas. Primeiro, verifica se o ID da carteira é fornecido,
    em seguida, verifica se a carteira existe para o usuário atual. Se a carteira existir, verifica se a carteira
    possui alguma transação associada. Se a carteira não possuir transações, ela é excluída do banco de dados.
    Se a carteira possuir transações, seu status é definido como 'S'.

    Parâmetros:
    - wallet_id (str): O ID da carteira a ser excluída. Este ID é obtido da solicitação POST do formulário.

    Retorna:
    - Se o ID da carteira não for fornecido, uma mensagem flash é exibida indicando que o ID da carteira não foi fornecido.
      O usuário é então redirecionado para a página de carteiras.
    - Se a carteira não existir para o usuário atual, uma mensagem flash é exibida indicando que a carteira não foi encontrada.
      O usuário é então redirecionado para a página de carteiras.
    - Se a carteira não possuir transações associadas, ela é excluída do banco de dados e uma mensagem flash é exibida indicando
      que a carteira foi excluída com sucesso. O usuário é então redirecionado para a página de carteiras.
    - Se a carteira possuir transações associadas, seu status é definido como 'S' e uma mensagem flash é exibida indicando que
      a carteira foi desativada devido às transações existentes. O usuário é então redirecionado para a página de carteiras.
    - Se ocorrer uma exceção durante as operações de banco de dados, uma reversão é executada, e uma mensagem flash é exibida indicando
      o erro que ocorreu. O usuário é então redirecionado para a página de carteiras.
    """
    wallet_id = request.form.get('wallet_id')
    if wallet_id:
        try:
            wallet = Wallet.query.filter_by(wallet_id=wallet_id, wallet_user_id=current_user.user_id).first()
            if not wallet:
                flash('Carteira não encontrada.', 'alert-danger')
                return redirect(url_for('views.wallets'))

            wallet_in_transactions = Transaction.query.filter(
                or_(
                    Transaction.payment_wallet_id == wallet_id,
                    Transaction.receiving_wallet_id == wallet_id
                )
            ).first()

            if not wallet_in_transactions:
                db.session.delete(wallet)
                db.session.commit()
                flash('Carteira excluída com sucesso.', 'alert-success')
            else:
                wallet.wallet_status = 'S'
                db.session.commit()
                flash('Carteira desativada pois já teve transações com ela.', 'alert-success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar desativar a carteira: {e}', 'alert-danger')
    else:
        flash("ID da carteira não fornecido", 'alert-danger')

    return redirect(url_for('views.wallets'))



# Adicionar Moeda
@crypto_wallet_bp.route('/add_crypto', methods=['GET', 'POST'])
@login_required
def add_crypto():
    """
    Esta função lida com a adição de uma nova criptomoeda. Primeiro, valida os dados do formulário, verifica se a criptomoeda
    já existe no banco de dados para o usuário atual e, em seguida, adiciona a nova criptomoeda ao banco de dados.

    Parâmetros:
    - formAddCrypto: Uma instância da classe AddCryptoForm, que contém os dados do formulário para adicionar uma criptomoeda.

    Retorna:
    - Se os dados do formulário são válidos e a criptomoeda não existe, uma nova criptomoeda é adicionada ao banco de dados,
      uma mensagem de flash de sucesso é exibida e o usuário é redirecionado para a página de criptomoedas.
    - Se os dados do formulário são inválidos ou a criptomoeda já existe, uma mensagem de flash de erro é exibida.
    - Se ocorre uma exceção durante as operações de banco de dados, uma reversão é executada e uma mensagem de flash de erro é exibida.
    """
    formAddCrypto = AddCryptoForm()
    if formAddCrypto.validate_on_submit():
        crypto_name = formAddCrypto.crypto_name.data.strip().upper()
        crypto_symbol = formAddCrypto.crypto_symbol.data.strip().upper()

        # Verificar se a criptomoeda já existe no banco de dados
        existing_crypto = Cryptocurrency.query.filter_by(crypto_name=crypto_name).first()

        if existing_crypto:
            flash(f'A criptomoeda {crypto_name} já existe no banco de dados.', 'alert-warning')
            return redirect(url_for('views.cryptos'))

        try:
            # Adiciona a nova criptomoeda ao banco de dados
            crypto = Cryptocurrency(crypto_name=crypto_name, crypto_symbol=crypto_symbol)
            db.session.add(crypto)
            db.session.commit()
            flash(f'A Criptomoeda {crypto_name} foi adicionada com sucesso', 'alert-success')
            return redirect(url_for('views.cryptos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar adicionar a criptomoeda: {e}', 'alert-danger')
        return redirect(url_for('views.cryptos'))

    return render_template('operacoes/add_crypto.html', formAddCrypto=formAddCrypto)




# Remover Moeda
@crypto_wallet_bp.route('/delete_crypto', methods=['POST'])
@login_required
def delete_crypto():
    """
    Esta função lida com a exclusão de uma criptomoeda. Primeiro, verifica se o crypto_id é fornecido,
    em seguida, verifica se a criptomoeda existe no banco de dados para o usuário atual. Se a criptomoeda existir,
    verifica se a criptomoeda possui alguma transação associada. Se a criptomoeda não possuir transações,
    ela é excluída do banco de dados. Se a criptomoeda possuir transações, seu status é definido como 'S'.

    Parâmetros:
    - crypto_id (str): O ID da criptomoeda a ser excluída. Este ID é obtido da solicitação POST do formulário.

    Retorna:
    - Se o crypto_id não for fornecido, uma mensagem flash é exibida indicando que o crypto_id não foi fornecido.
      O usuário é então redirecionado para a página de criptomoedas.
    - Se a criptomoeda não for encontrada para o usuário atual, uma mensagem flash é exibida indicando que a criptomoeda não foi encontrada.
      O usuário é então redirecionado para a página de criptomoedas.
    - Se a criptomoeda não possuir transações associadas, ela é excluída do banco de dados e uma mensagem flash é exibida indicando
      que a criptomoeda foi excluída com sucesso. O usuário é então redirecionado para a página de criptomoedas.
    - Se a criptomoeda possuir transações associadas, seu status é definido como 'S' e uma mensagem flash é exibida indicando que
      a criptomoeda foi desativada devido às transações existentes. O usuário é então redirecionado para a página de criptomoedas.
    - Se ocorrer uma exceção durante as operações de banco de dados, uma reversão é executada e uma mensagem flash é exibida indicando
      o erro que ocorreu. O usuário é então redirecionado para a página de criptomoedas.
    """
    crypto_id = request.form.get('crypto_id')
    if crypto_id:
        try:
            crypto = Cryptocurrency.query.filter_by(crypto_id=crypto_id).first()
            if not crypto:
                flash('Criptomoeda não encontrada.', 'alert-danger')
                return redirect(url_for('views.cryptos'))

            crypto_in_transaction = Transaction.query.filter(
                or_(
                    Transaction.crypto_payment_id == crypto.crypto_id,
                    Transaction.crypto_receive_id == crypto.crypto_id,
                    Transaction.crypto_fee_id == crypto.crypto_id
                )
            ).first()

            if not crypto_in_transaction:
                db.session.delete(crypto)
                db.session.commit()
                flash('Criptomoeda excluída com sucesso.', 'alert-success')
            else:
                crypto.crypto_status = 'S'
                db.session.commit()
                flash('Criptomoeda apenas desativada, pois teve transações com ela.', 'alert-success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao tentar desativar a criptomoeda: {e}', 'alert-danger')
    else:
        flash("ID da criptomoeda não fornecido", 'alert-danger')

    return redirect(url_for('views.cryptos'))



