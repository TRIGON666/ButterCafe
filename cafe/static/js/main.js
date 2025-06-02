// Анимация появления header и меню
window.addEventListener('DOMContentLoaded', function() {
    var burger = document.querySelector('.burger');
    var nav = document.querySelector('.main-nav');
    var overlay = document.getElementById('menuOverlay');
    // Гарантируем, что меню закрыто при загрузке
    if (burger) burger.classList.remove('open');
    if (nav) nav.classList.remove('open');
    if (overlay) overlay.classList.remove('active');

    function closeMenu() {
        nav.classList.remove('open');
        burger.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
    }
    if (burger && nav) {
        burger.addEventListener('click', function(e) {
            e.stopPropagation();
            nav.classList.toggle('open');
            burger.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
        });
        nav.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                closeMenu();
            });
        });
        if (overlay) {
            overlay.addEventListener('click', function() {
                closeMenu();
            });
        }
        document.addEventListener('click', function(e) {
            if (nav.classList.contains('open')) {
                if (!nav.contains(e.target) && !burger.contains(e.target)) {
                    closeMenu();
                }
            }
        });
    }
});

// Здесь можно добавить другие JS-функции для сайта:
// - бургер-меню для мобильных
// - всплывающие сообщения (alert/toast)
// - модальные окна (например, для заказа)
// - плавный скролл к якорям
// - обработка форм (AJAX)
// - динамическое обновление корзины 