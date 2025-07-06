from flask import Blueprint, render_template, flash, redirect, url_for, request
from criptoControl.forms import Users, RegisterForm
from criptoControl.models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
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
        if user and check_password_hash(user.password_hash, formLogin.password.data):
            # Se o email e a senha são válidos, faz o login do usuário
            login_user(user, remember=formLogin.remember_me.data)
            return redirect(url_for('main.index'))  # Redireciona para a rota index após o login
        else:
            flash('Credenciais inválidas. Verifique seu email e/ou senha.', 'danger')

    return render_template('auth/login.html', formLogin=formLogin)


@auth_bp.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """
    Lida com o cadastro de novos usuários.

    Rota: '/create_account'
    Métodos HTTP: GET, POST

    Esta função gerencia o processo de criação de uma nova conta de usuário:
    - Renderiza um formulário de registro para entrada de dados do usuário (username, email, senha).
    - Valida os dados submetidos no formulário.
    - Verifica se o e-mail já está registrado no banco de dados.
    - Se o e-mail for único:
        - Cria um novo registro de usuário com as informações fornecidas.
        - Armazena o hash da senha no banco de dados.
        - Salva o novo usuário na sessão do banco de dados.
        - Loga automaticamente o usuário após o cadastro.
        - Redireciona para a página inicial com uma mensagem de boas-vindas.
    - Se o e-mail já estiver registrado:
        - Exibe uma mensagem de erro informando que o e-mail já está cadastrado.
        - Redireciona o usuário de volta para a página de cadastro.

    Retornos:
        - Renderiza a página de cadastro com o formulário (GET).
        - Redireciona para a página inicial ou para a página de cadastro, dependendo da validação dos dados (POST).
    """
    form = RegisterForm()

    if form.validate_on_submit():
        # Verificar se o e-mail já está registrado
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('O email já está cadastrado. Tente outro.', 'danger')
            return redirect(url_for('auth.create_account'))

        # Criar novo usuário
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(new_user)
        db.session.commit()

        # Logar automaticamente após o cadastro
        flash('Conta criada com sucesso! Bem-vindo!', 'success')
        login_user(new_user)
        return redirect(url_for('main.index'))

    # Renderizar a página de cadastro
    return render_template('auth/register.html', form=form)


# terminar de impelmentar e descomentar o html
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """
    Rota para recuperação de senha.
    """
    # Implemente a lógica para enviar email de recuperação ou exibir instruções
    flash("Função de recuperação de senha não implementada ainda.", "alert-info")
    return redirect(url_for('auth.login'))
