// js/agenda.js
document.addEventListener('DOMContentLoaded', function() {
    const diasWrapper = document.querySelector('.dias-wrapper');
    if (!diasWrapper) return;

    diasWrapper.addEventListener('click', function(e) {
        const diaCard = e.target.closest('.dia-card');
        if (!diaCard) return;

        // Encontra o contêiner de eventos específico deste card
        const eventosDoDia = diaCard.nextElementSibling;
        const jaEstaAberto = eventosDoDia.classList.contains('show');

        // Fecha todos os outros itens abertos
        diasWrapper.querySelectorAll('.dia-item-wrapper').forEach(wrapper => {
            const card = wrapper.querySelector('.dia-card');
            const eventos = wrapper.querySelector('.eventos-do-dia');

            if (eventos !== eventosDoDia) {
                card.classList.remove('active');
                eventos.classList.remove('show');
                eventos.style.maxHeight = null; // Reseta a altura para a animação de fechar
            }
        });

        // Alterna o estado do item clicado
        diaCard.classList.toggle('active');
        eventosDoDia.classList.toggle('show');

        // Anima a altura de forma fluida
        if (eventosDoDia.classList.contains('show')) {
            // Define max-height para a altura real do conteúdo para a animação de abrir
            eventosDoDia.style.maxHeight = eventosDoDia.scrollHeight + "px";
        } else {
            // Reseta a altura para a animação de fechar
            eventosDoDia.style.maxHeight = null;
        }
    });
});