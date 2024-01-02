document.addEventListener('DOMContentLoaded', function () {
    const menuHeader = document.querySelector('.menu-header');
    const mainMenu = document.getElementById('main-menu');
    const menuContainer = document.querySelector('.menu-container');

    menuHeader.addEventListener('click', function () {
        menuHeader.classList.toggle('menu-opened');
        menuContainer.classList.toggle('menu-closed', !menuHeader.classList.contains('menu-opened'));

        if (menuHeader.classList.contains('menu-opened')) {
            mainMenu.style.display = 'block';
            setTimeout(() => {
                mainMenu.style.opacity = '1';
                mainMenu.style.maxHeight = '500px';
            }, 0);
        } else {
            mainMenu.style.opacity = '0';
            mainMenu.style.maxHeight = '0';
            setTimeout(() => {
                mainMenu.style.display = 'none';
            }, 300);
        }
    });

    document.addEventListener('click', function (event) {
        if (!menuContainer.contains(event.target)) {
            menuHeader.classList.remove('menu-opened');
            menuContainer.classList.add('menu-closed');
            mainMenu.style.opacity = '0';
            mainMenu.style.maxHeight = '0';
            setTimeout(() => {
                mainMenu.style.display = 'none';
            }, 300);
        }
    });

    menuContainer.addEventListener('mouseleave', function () {
        menuHeader.classList.remove('menu-opened');
        menuContainer.classList.add('menu-closed');
        mainMenu.style.opacity = '0';
        mainMenu.style.maxHeight = '0';
        setTimeout(() => {
            mainMenu.style.display = 'none';
        }, 300);
    });

    window.addEventListener('scroll', function () {
        menuHeader.classList.remove('menu-opened');
        menuContainer.classList.add('menu-closed');
        mainMenu.style.opacity = '0';
        mainMenu.style.maxHeight = '0';
        setTimeout(() => {
            mainMenu.style.display = 'none';
        }, 300);
    });
});
