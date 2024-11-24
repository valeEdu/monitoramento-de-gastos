// scripts.js

// Function to handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('transaction-form');

    if (form) {
        form.addEventListener('submit', function(event) {
            // Perform basic validation
            const description = document.getElementById('description').value;
            const amount = document.getElementById('amount').value;

            if (description.trim() === '' || amount.trim() === '') {
                event.preventDefault(); // Prevent form submission
                alert('Por favor, preencha todos os campos.');
            }
        });
    }

    // Function to confirm deletion of a transaction
    const deleteLinks = document.querySelectorAll('.delete-transaction');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const confirmation = confirm('Tem certeza que deseja excluir esta transação?');
            if (!confirmation) {
                event.preventDefault(); // Prevent the default action if not confirmed
            }
        });
    });
});

// Example of an AJAX request to fetch transactions
function fetchTransactions() {
    fetch('/api/transactions')
        .then(response => response.json())
        .then(data => {
            const transactionsTable = document.getElementById('transactions-table-body');
            transactionsTable.innerHTML = ''; // Clear existing rows

            data.forEach(transaction => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${transaction.id}</td>
                    <td>${transaction.description}</td>
                    <td>${transaction.category}</td>
                    <td>${transaction.amount}</td>
                    <td>${new Date(transaction.date).toLocaleDateString()}</td>
                    <td>
                        <a href="/edit/${transaction.id}">Editar</a>
                        <a href="/delete/${transaction.id}" class="delete-transaction">Excluir</a>
                    </td>
                `;
                transactionsTable.appendChild(row);
            });
        })
        .catch(error => console.error('Erro ao buscar transações:', error));
}

// Call fetchTransactions on page load if needed
document.addEventListener('DOMContentLoaded', fetchTransactions);