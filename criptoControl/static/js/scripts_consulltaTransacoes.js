// Adiciona um evento que será acionado quando o conteúdo do DOM estiver completamente carregado
document.addEventListener('DOMContentLoaded', function() {
    /**
     * Calcula o total pago para uma linha da tabela.
     * 
     * @param {HTMLElement} row - A linha da tabela que contém os dados da transação.
     */
    function calculartotal_paid(row) {
        // Obtém os valores dos campos da linha, convertendo-os para números
        var quantidade = parseFloat(row.querySelector('.quantidade').innerText) || 0; // Quantidade da criptomoeda
        var preco = parseFloat(row.querySelector('.preco').innerText) || 0; // Preço da criptomoeda
        var totalMoeda = parseFloat(row.querySelector('.total-crypto').innerText) || 0; // Total da moeda
        var total_fee = parseFloat(row.querySelector('.total-taxa').innerText) || 0; // Total das taxas

        // Log para depuração
        console.log('Quantidade:', quantidade);
        console.log('Preço:', preco);
        console.log('Total Moeda:', totalMoeda);
        console.log('Total Taxa:', total_fee);

        // Calcula o total da transação somando o total da moeda e o total das taxas
        var total_paid = totalMoeda + total_fee;

        // Atualiza o campo Total Transação na linha correspondente
        var totalTransacaoElement = row.querySelector('.total-transacao');
        if (totalTransacaoElement) {
            totalTransacaoElement.innerText = total_paid.toFixed(2); // Formata o total para duas casas decimais
        } else {
            console.error('Elemento para total-transacao não encontrado.'); // Mensagem de erro se o elemento não for encontrado
        }
    }

    // Obtém todas as linhas da tabela
    var linhas = document.querySelectorAll('table tbody tr');

    // Verificação de linhas encontradas
    if (linhas.length === 0) {
        console.error('Nenhuma linha encontrada na tabela.'); // Mensagem de erro se não houver linhas
    } else {
        // Itera sobre as linhas e calcula o total para cada uma
        linhas.forEach(function(linha) {
            calculartotal_paid(linha); // Chama a função para calcular o total pago
        });
    }
});
