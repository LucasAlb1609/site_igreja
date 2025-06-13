// js/agenda.js
document.addEventListener('DOMContentLoaded', function() {
    const diasWrapper = document.querySelector('.dias-wrapper');
    const eventosContainer = document.querySelector('.eventos-container');

    if (!diasWrapper) return;

    diasWrapper.addEventListener('click', function(e) {
        const diaCard = e.target.closest('.dia-card');
        if (!diaCard) return;

        const targetId = diaCard.dataset.target;
        const targetEventos = document.querySelector(targetId);

        // Remove a classe 'active' de todos os cards
        diasWrapper.querySelectorAll('.dia-card').forEach(card => {
            card.classList.remove('active');
        });

        // Esconde todos os containers de eventos
        eventosContainer.querySelectorAll('.eventos-do-dia').forEach(container => {
            container.classList.remove('show');
        });

        // Se o container alvo já estava visível, esconde-o. Senão, mostra-o.
        if (targetEventos.classList.contains('show')) {
            targetEventos.classList.remove('show');
        } else {
            targetEventos.classList.add('show');
            diaCard.classList.add('active'); // Adiciona classe 'active' ao card clicado
        }
    });
});