// Função para redirecionar para o link em uma nova guia
function redirectToLinkInNewTab(link) {
    window.open(link, '_blank');
}

// Adiciona um ouvinte de evento para cada item do dropdown
document.querySelectorAll('.dropdown-item').forEach(function(item) {
    item.addEventListener('click', function(event) {
    });
});

// Adiciona um ouvinte de evento para o item "História"
document.querySelector('.dropdown-item[href="historia.html"]').addEventListener('click', function(event) {
    event.preventDefault(); // Impede o comportamento padrão do link
    var link = this.getAttribute('href'); // Obtém o atributo href do link
    window.location.href = link; // Redireciona para a subpágina "historia.html"
});