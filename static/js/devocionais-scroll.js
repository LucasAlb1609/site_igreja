document.addEventListener("DOMContentLoaded", function() {
    // Rolagem suave para as âncoras do índice de devocionais
    document.querySelectorAll('.devocional-indice a').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
  
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
  
        if (targetElement) {
          // Leva em consideração a altura do cabeçalho fixo para não cobrir o título
          const headerOffset = 80; // Ajuste este valor conforme a altura do seu cabeçalho
          const elementPosition = targetElement.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        
          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
          });
        }
      });
    });
  });