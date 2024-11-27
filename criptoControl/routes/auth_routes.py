from flask import Blueprint, render_template, flash, redirect, url_for
from criptoControl.forms import Users
from criptoControl.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user


auth_bp = Blueprint('auth', __name__)


#---------------   Autentication   --------------------

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    '''
    Lida com o login do usuário.

    Esta função renderiza uma página de login e manipula a autenticação do usuário.
    Ela utiliza um formulário para coletar as credenciais do usuário e as verifica contra o banco de dados.
    Se as credenciais são válidas, o usuário é logado e redirecionado para a página principal.
    Se as credenciais são inválidas, uma mensagem de erro é exibida.

    auth_bp = Blueprint('auth', __name__)
    Parâmetros:
    None
    '''
    formLogin = Users()  # Formulário de login

    if formLogin.validate_on_submit():
        # Verifica se o email existe no banco de dados
        user = User.query.filter_by(email=formLogin.email.data).first()
        if user and check_password_hash(user.password_hash, formLogin.password_hash.data):
            # Se o email e a senha são válidos, faz o login do usuário
            login_user(user)
            return redirect(url_for('main.index'))  # Redireciona para a rota index após o login
        else:
            flash('Credenciais inválidas. Verifique seu email e/ou senha.', 'alert-danger')

    return render_template('auth/login.html', formLogin=formLogin)


