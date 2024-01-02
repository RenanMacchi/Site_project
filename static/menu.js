document.addEventListener('DOMContentLoaded', function () {
    const menuHeader = document.querySelector('.menu-header');
    const mainMenu = document.getElementById('main-menu');

    menuHeader.addEventListener('click', function () {
        mainMenu.style.display = mainMenu.style.display === 'block' ? 'none' : 'block';
        menuHeader.classList.toggle('menu-opened');
    });

    // Fechar o menu se clicar fora dele
    document.addEventListener('click', function (event) {
        if (!menuHeader.contains(event.target) && !mainMenu.contains(event.target)) {
            mainMenu.style.display = 'none';
            menuHeader.classList.remove('menu-opened');
        }
    });
});
