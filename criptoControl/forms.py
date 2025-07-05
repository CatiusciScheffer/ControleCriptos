from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, DateField, BooleanField
from wtforms.validators import DataRequired, Optional, Email, Length, ValidationError, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
import re


class TransactionsForm(FlaskForm):
    """
    Formulário para registrar e gerenciar transações financeiras envolvendo criptomoedas.

    Atributos:
        transaction_type (SelectField): Campo para selecionar o tipo de transação (Compra, Venda, Transferência ou Saldo), obrigatório.
        crypto_payment (SelectField): Campo para selecionar a criptomoeda utilizada como pagamento, opcional.
        crypto_payment_price (FloatField): Campo para informar o preço atual da criptomoeda de pagamento, opcional.
        crypto_payment_quantity (FloatField): Campo para informar a quantidade de criptomoeda de pagamento, opcional.
        total_paid (FloatField): Campo para calcular ou informar o valor total pago, opcional.
        crypto_fee (SelectField): Campo para selecionar a criptomoeda utilizada para taxas, opcional.
        crypto_fee_price (FloatField): Campo para informar o preço atual da criptomoeda de taxa, opcional.
        crypto_fee_quantity (FloatField): Campo para informar a quantidade de criptomoeda utilizada como taxa, opcional.
        total_fee (FloatField): Campo para calcular ou informar o valor total da taxa, opcional.
        crypto_receive (SelectField): Campo para selecionar a criptomoeda recebida, opcional.
        crypto_receive_price (FloatField): Campo para informar o preço atual da criptomoeda recebida, opcional.
        crypto_receive_quantity (FloatField): Campo para informar a quantidade de criptomoeda recebida, opcional.
        total_received (FloatField): Campo para calcular ou informar o valor total recebido, opcional.
        payment_wallet (SelectField): Campo para selecionar a carteira de onde sairá o pagamento, opcional.
        receiving_wallet (SelectField): Campo para selecionar a carteira que receberá o pagamento, opcional.
        transaction_date (DateField): Campo para informar a data da transação, opcional.
        btn_add_transactions (SubmitField): Botão para enviar os dados do formulário e adicionar a transação.
    """
    transaction_type = SelectField('Tipo Transação', choices=[('','Selecione o Tipo'), ('Compra','Compra'), ('Venda','Venda'), ('Transferência','Transferência'), ('Saldo','Saldo')], validators=[DataRequired()])
    crypto_payment = SelectField('Moeda', choices=[],validators=[Optional()])
    crypto_payment_price = FloatField('Preço Atual', validators=[Optional()])
    crypto_payment_quantity = FloatField('Quantidade', validators=[Optional()])
    total_paid = FloatField('Total Transação', validators=[Optional()])
    crypto_fee = SelectField('Moeda Taxa', choices=[], validators=[Optional()])
    crypto_fee_price = FloatField('Preço Atual', validators=[Optional()])
    crypto_fee_quantity = FloatField('Quantidade', validators=[Optional()])
    total_fee = FloatField('Total Taxa', validators=[Optional()])
    crypto_receive = SelectField('Moeda Recebida', choices=[],validators=[Optional()])
    crypto_receive_price = FloatField('Preço Atual', validators=[Optional()])
    crypto_receive_quantity = FloatField('Quantidade', validators=[Optional()])
    total_received = FloatField('Total Recebido', validators=[Optional()])
    payment_wallet = SelectField('Carteira Saída', choices=[], validators=[Optional()])
    receiving_wallet = SelectField('Carteira Recebimento', choices=[], validators=[Optional()])
    transaction_date = DateField('Data da Transação', format='%Y-%m-%d', validators=[Optional()])
    btn_add_transactions = SubmitField('Adicionar')


class AddWalletForm(FlaskForm):
    """
    Formulário para adicionar uma nova carteira no sistema.

    Atributos:
        wallet_name (StringField): Campo de texto para o nome da carteira, obrigatório.
        wallet_network (StringField): Campo de texto para a rede da carteira, obrigatório.
    """
    wallet_name = StringField('Nome', validators=[DataRequired()])
    wallet_network = StringField('Rede', validators=[DataRequired()])

class AddCryptoForm(FlaskForm):
    """
    Classe de formulário para adicionar uma nova criptomoeda.

    Esta classe define um formulário utilizado para a entrada de dados de uma nova criptomoeda, incluindo
    o nome e o símbolo da criptomoeda. Os campos possuem validações para garantir que os dados inseridos
    sejam obrigatórios.

    Atributos:
        crypto_name (StringField): Campo para o nome da criptomoeda. Deve ser preenchido.
        crypto_symbol (StringField): Campo para o símbolo da criptomoeda. Deve ser preenchido.

    Validações:
        - O campo de nome da criptomoeda deve ser preenchido.
        - O campo de símbolo da criptomoeda deve ser preenchido.

    Exemplos de uso:
        form = AddCryptoForm()
        if form.validate_on_submit():
            # Lógica para adicionar a nova criptomoeda
    """
    crypto_name = StringField('Nome', validators=[DataRequired()])
    crypto_symbol = StringField('Símbolo', validators=[DataRequired()])

def check_password_complexity(form, field):
    """
    Verifica a complexidade da senha fornecida.

    Esta função é utilizada como um validador para garantir que a senha atenda a critérios de complexidade
    específicos. A função verifica se a senha contém pelo menos uma letra maiúscula e pelo menos um caractere
    especial.

    Parâmetros:
        form (FlaskForm): O formulário que contém o campo da senha.
        field (Field): O campo da senha que está sendo validado.

    Levanta:
        ValidationError: Se a senha não contiver pelo menos uma letra maiúscula ou um caractere especial.

    Exemplo de uso:
        # Esta função pode ser usada como um validador em um campo de senha em um formulário Flask.
        password_hash = PasswordField('Senha', validators=[DataRequired(), check_password_complexity])
    """
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('A senha deve conter pelo menos uma letra maiúscula.')
    if not re.search(r'[\W_]', password): 
        raise ValidationError('A senha deve conter pelo menos um caractere especial.')

class Users(FlaskForm):
    """
    Formulário de autenticação de usuários.

    Este formulário é utilizado para realizar operações de login, cadastro de novas contas e recuperação de senha.

    Campos:
        - email (StringField): Campo para o e-mail do usuário.
            - Obrigatório.
            - Deve ser um endereço de e-mail válido.
        - password_hash (PasswordField): Campo para a senha do usuário.
            - Obrigatório.
            - Deve ter no mínimo 8 caracteres.
            - Valida a complexidade da senha utilizando `check_password_complexity`.
        - remember_me (BooleanField): Checkbox para lembrar a sessão do usuário.
            - Opcional.
        - btn_user_enter (SubmitField): Botão para realizar o login.
        - btn_user_create (SubmitField): Botão para criar uma nova conta.
        - release_cta (SubmitField): Botão para recuperação de senha.

    Validações:
        - O campo 'email' exige um e-mail válido.
        - O campo 'password_hash' requer pelo menos 8 caracteres e deve passar na validação de complexidade.
        - Todos os campos obrigatórios devem ser preenchidos antes do envio do formulário.

    Uso:
        Este formulário é utilizado em páginas relacionadas à autenticação, como login, cadastro e recuperação de senha.

    Observação:
        A validação de complexidade da senha é realizada pela função `check_password_complexity`.
    """
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Insira um email válido.")
        ]
    )
    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(message="O campo senha é obrigatório."),
        ]
    )
    remember_me = BooleanField('Lembrar-me')
    btn_user_enter = SubmitField('Entrar')
    btn_user_create = SubmitField('Cadastrar')
    release_cta = SubmitField('Esqueci minha senha')
    

class RegisterForm(FlaskForm):
    """
    Formulário de registro de novos usuários.

    Este formulário é usado para capturar e validar os dados necessários para o registro de um novo usuário no sistema.

    Campos:
        - username: Campo de texto para o nome completo do usuário. É obrigatório.
            - Validações:
                - `DataRequired`: Certifica-se de que o campo não está vazio.
        - email: Campo de texto para o email do usuário. É obrigatório e deve ser um endereço de email válido.
            - Validações:
                - `DataRequired`: Certifica-se de que o campo não está vazio.
                - `Email`: Garante que o valor inserido é um email válido.
        - password: Campo para a senha do usuário. É obrigatório e deve ter pelo menos 6 caracteres.
            - Validações:
                - `DataRequired`: Certifica-se de que o campo não está vazio.
                - `Length`: Garante que a senha tenha no mínimo 6 caracteres.
        - confirm_password: Campo para confirmar a senha do usuário. É obrigatório e deve corresponder ao valor do campo `password`.
            - Validações:
                - `DataRequired`: Certifica-se de que o campo não está vazio.
                - `EqualTo`: Garante que o valor corresponde ao campo `password`.
        - submit: Botão para enviar o formulário.

    Uso:
        Este formulário é renderizado em templates para capturar as informações do usuário e validá-las antes de criar um novo registro no banco de dados.

    Exemplo:
        >>> form = RegisterForm()
        >>> form.validate_on_submit()
    """
    
    username = StringField(
        'Nome Completo',
        validators=[
            DataRequired(message="O campo 'Nome Completo' é obrigatório.")
        ],
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="O campo email é obrigatório."),
            Email(message="Insira um email válido."),
        ],
    )
    password = PasswordField(
        'Senha',
        validators=[
            DataRequired(message="O campo senha é obrigatório."),
            Length(min=6, message="A senha deve ter no mínimo 6 caracteres."),
            check_password_complexity
        ],
    )
    confirm_password = PasswordField(
        'Confirme sua senha',
        validators=[
            DataRequired(message="O campo de confirmação de senha é obrigatório."),
            EqualTo('password', message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField('Cadastrar')
