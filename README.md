# **Gerenciador de Criptomoedas**  
Este é um aplicativo de gerenciamento de criptomoedas desenvolvido com **Flask**, projetado para ajudar usuários a rastrear suas transações, saldos e carteiras. Ideal para entusiastas de cripto e traders, o sistema também inclui suporte para cálculos de taxas e integração com preços dinâmicos.  

---

## 🚀 **Funcionalidades**  

### **Gerenciamento de Carteiras**  
- Criação, edição e exclusão de carteiras.  
- Após o login, o primeiro passo é criar uma carteira.  
- Verifique se a moeda desejada já está cadastrada; caso contrário, cadastre-a.  

### **Controle de Transações**  
- Registre **compras**, **vendas**, **transferências** e **adições de saldo**.  
- O sistema valida saldos automaticamente para evitar transações inválidas.  
- Suporte para reversão de transações.  

### **Atualização de Preços**  
- Atualize os preços das criptomoedas em tempo real por meio de uma integração dedicada.  

### **Relatórios Detalhados e Análises**  
- Histórico completo de transações, com cálculos automáticos de taxas e totais.  
- Ferramentas para análises de DCA (*Dollar Cost Averaging*), lucro e prejuízo.  

### **Exportação para Declaração Tributária** *(Em breve)*  
- Em breve, será possível gerar um arquivo compatível com o site da Receita Federal do Brasil (RFB) para facilitar a **Declaração de Bens e Direitos**.  

---

## 🛠️ **Tecnologias Utilizadas**  

### **Backend**  
- Flask  
- SQLAlchemy  

### **Frontend**  
- HTML  
- CSS  
- Bootstrap  

### **Banco de Dados**  
- SQLite  

### **Outras Bibliotecas**  
- Flask-WTF  
- WTForms  

---

## 🗂️ **Estrutura do Projeto**  

```plaintext
CRYPTOS_FLASK/
├── criptoControl/  
│   ├── routes/  
│   │   ├── __init__.py  
│   │   ├── auth_routes.py  
│   │   ├── crud_crypto_wallet.py  
│   │   ├── main_routes.py  
│   │   ├── transactions_routes.py  
│   │   ├── update_price.py  
│   │   └── views_databases.py  
│   ├── static/  
│   │   ├── css/  
│   │   │   └── style.css  
│   │   ├── js/  
│   │   │   ├── scripts_consultaTransacoes.js  
│   │   │   └── scripts_transacoes.js  
│   ├── templates/  
│   │   ├── auth/  
│   │   │   ├── login.html  
│   │   │   └── register.html  
│   │   ├── operacoes/  
│   │   │   ├── add_crypto.html  
│   │   │   ├── add_transactions.html  
│   │   │   ├── add_wallet.html  
│   │   │   ├── cryptos.html  
│   │   │   ├── modal_confirm_delete.html  
│   │   │   ├── transactions.html  
│   │   │   └── wallets.html  
│   │   ├── views_databases/  
│   │   │   ├── crypto_DCA.html  
│   │   │   ├── crypto_lucroXprejuizo.html  
│   │   │   ├── filtros_transacoes.html  
│   │   │   ├── prices.html  
│   │   │   ├── transacoes_filtradas.html  
│   │   │   ├── wallet_balances.html  
│   │   │   └── wallet_summary.html  
│   │   ├── index.html  
│   │   └── navibar.html  
│   ├── __init__.py  
│   ├── api.py  
│   ├── forms.py  
│   └── models.py  
├── env/  
├── instance/  
│   └── crypto_data.db  
├── main.py  
└── requirements.txt  
```
## ⚙️ **Instalação e Execução**  

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/CatiusciScheffer/ControleCriptos
  
## 🌐 **Demonstração Online**
Acesse o projeto hospedado em: [Adicione aqui o link para o seu perfil no LinkedIn, se desejar.](https://controlecripto-18636635ed0d.herokuapp.com/)
Controle Criptos

Login para teste:
- E-mail: catiusci.ctadigital@gmail.com
- Senha: Chefa220408#
Ou crie sua própria conta para explorar!

## 📬 **Contato**
E-mail: cpcscheffer@outlook.com
LinkedIn: [Adicione aqui o link para o seu perfil no LinkedIn, se desejar.](https://www.linkedin.com/in/catiuscipagnonceli-cienciasdacomputacao/)
