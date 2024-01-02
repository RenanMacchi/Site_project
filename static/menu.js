document.addEventListener('DOMContentLoaded', function () {
    const menuHeader = document.querySelector('.menu-header');
    const mainMenu = document.getElementById('main-menu');
    const menuContainer = document.querySelector('.menu-container');

    menuHeader.addEventListener('click', function () {
        mainMenu.style.display = mainMenu.style.display === 'block' ? 'none' : 'block';
        menuHeader.classList.toggle('menu-opened');
        menuContainer.classList.toggle('menu-closed', mainMenu.style.display === 'none');
    });

    // Fechar o menu se clicar fora dele
    document.addEventListener('click', function (event) {
        if (!menuContainer.contains(event.target)) {
            mainMenu.style.display = 'none';
            menuHeader.classList.remove('menu-opened');
            menuContainer.classList.add('menu-closed');
        }
    });

    // Fechar o menu ao sair do menu
    menuContainer.addEventListener('mouseleave', function () {
        mainMenu.style.display = 'none';
        menuHeader.classList.remove('menu-opened');
        menuContainer.classList.add('menu-closed');
    });

    // Fechar o menu ao rolar a página
    window.addEventListener('scroll', function () {
        mainMenu.style.display = 'none';
        menuHeader.classList.remove('menu-opened');
        menuContainer.classList.add('menu-closed');
    });
});
