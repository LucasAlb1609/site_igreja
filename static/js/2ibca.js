// Função para redirecionar para o link em uma nova guia
function redirectToLinkInNewTab(link) {
    window.open(link, '_blank');
}

// Função segura para adicionar event listeners
function safeAddListener(selector, event, handler) {
    const element = document.querySelector(selector);
    if (element) {
        element.addEventListener(event, handler);
    }
}

// Adiciona ouvintes de evento de forma segura
document.addEventListener('DOMContentLoaded', function() {
    // Dropdown items
    document.querySelectorAll('.dropdown-item').forEach(function(item) {
        item.addEventListener('click', function(event) {
            // Comportamento padrão já funciona com Bootstrap
        });
    });

    // História link - apenas se existir
    safeAddListener('.dropdown-item[href="historia.html"]', 'click', function(event) {
        event.preventDefault();
        window.location.href = this.getAttribute('href');
    });

    // Efeitos de hover para os cards de pessoas
    const pessoaCards = document.querySelectorAll('.pessoa-card');
    
    if (pessoaCards.length > 0) {
        pessoaCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px)';
                card.style.boxShadow = '0 10px 20px rgba(0,0,0,0.2)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
            });
        });
    }
    
    // Alternativa para páginas carregadas via AJAX
    if (document.readyState === 'complete') {
        document.dispatchEvent(new Event('DOMContentLoaded'));
    }
});