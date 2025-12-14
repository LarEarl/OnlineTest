// Мобильное меню
document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.menu-toggle');
  const navLeft = document.querySelector('.nav-left');
  
  if (menuToggle && navLeft) {
    menuToggle.addEventListener('click', function() {
      menuToggle.classList.toggle('active');
      navLeft.classList.toggle('active');
    });

    // Закрываем меню при клике вне его
    document.addEventListener('click', function(event) {
      if (!event.target.closest('header nav')) {
        menuToggle.classList.remove('active');
        navLeft.classList.remove('active');
      }
    });

    // Закрываем меню при изменении размера окна
    window.addEventListener('resize', function() {
      if (window.innerWidth > 768) {
        menuToggle.classList.remove('active');
        navLeft.classList.remove('active');
      }
    });
  }
});
