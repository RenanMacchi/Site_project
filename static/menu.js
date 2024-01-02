document.addEventListener('DOMContentLoaded', function () {
    const menuHeader = document.querySelector('.menu-header');
    const mainMenu = document.getElementById('main-menu');

    menuHeader.addEventListener('click', function () {
        mainMenu.style.display = (mainMenu.style.display === 'block') ? 'none' : 'block';
        menuHeader.classList.toggle('menu-opened');
    });
});