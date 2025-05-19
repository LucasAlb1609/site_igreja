// Controle do menu mobile
document.addEventListener('DOMContentLoaded', function() {
    // Se o botão de menu hamburger não existir, criá-lo dinamicamente
    if (!document.querySelector('.menu-toggle')) {
        const header = document.querySelector('header');
        const nav = document.querySelector('nav');
        
        // Criar o botão hamburger
        const menuToggle = document.createElement('div');
        menuToggle.className = 'menu-toggle';
        menuToggle.innerHTML = '<span></span><span></span><span></span>';
        
        // Inserir antes do nav
        header.insertBefore(menuToggle, nav);
    }
    
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.menu');
    
    // Função para verificar o tamanho da tela e ajustar o menu
    function checkScreenSize() {
        if (window.innerWidth <= 576) {
            // Em mobile, esconde o menu e adiciona o botão hamburger
            menu.classList.remove('show');
            menuToggle.style.display = 'block';
        } else {
            // Em telas maiores, força o menu a ser visível e esconde o botão
            menu.classList.remove('show');
            menu.style.display = '';
            menuToggle.style.display = 'none';
            
            // Resetar todos os dropdowns ao mudar para desktop
            document.querySelectorAll('.nav-item.show').forEach(function(item) {
                item.classList.remove('show');
            });
        }
    }
    
    // Executar na inicialização
    checkScreenSize();
    
    // Atualizar ao redimensionar a janela
    window.addEventListener('resize', checkScreenSize);
    
    // Alternar menu ao clicar no hamburger
    menuToggle.addEventListener('click', function() {
        menu.classList.toggle('show');
    });
    
    // Fechar o menu ao clicar fora dele (em mobile)
    document.addEventListener('click', function(event) {
        const isMenuToggle = event.target.closest('.menu-toggle');
        const isMenu = event.target.closest('.menu');
        
        if (!isMenuToggle && !isMenu && menu.classList.contains('show')) {
            menu.classList.remove('show');
            
            // Também fechar todos os dropdowns abertos
            document.querySelectorAll('.nav-item.show').forEach(function(item) {
                item.classList.remove('show');
            });
        }
    });
    
    // Controlar os dropdowns em dispositivos móveis
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(event) {
            if (window.innerWidth <= 576) {
                event.preventDefault();
                event.stopPropagation(); // Impedir que o evento se propague para outros elementos
                
                // Encontrar o item pai (nav-item)
                const navItem = toggle.closest('.nav-item');
                
                // Verificar se já está aberto
                const isOpen = navItem.classList.contains('show');
                
                // Fechar todos os outros dropdowns primeiro
                document.querySelectorAll('.nav-item.show').forEach(function(item) {
                    if (item !== navItem) {
                        item.classList.remove('show');
                    }
                });
                
                // Alternar o estado do dropdown atual (abrir se fechado, fechar se aberto)
                if (isOpen) {
                    navItem.classList.remove('show');
                } else {
                    navItem.classList.add('show');
                }
            }
        });
    });

    // Fechar submenu ao clicar em um item dentro do dropdown
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    
    dropdownItems.forEach(function(item) {
        item.addEventListener('click', function(event) {
            if (window.innerWidth <= 576) {
                // Impedir que o evento se propague
                event.stopPropagation();
                
                // Fecha o dropdown pai
                const parentDropdown = item.closest('.nav-item');
                if (parentDropdown) {
                    parentDropdown.classList.remove('show');
                }
                
                // Fecha o menu principal
                menu.classList.remove('show');
            }
        });
    });
}); 