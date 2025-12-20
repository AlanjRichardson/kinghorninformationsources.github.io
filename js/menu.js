<!-- Existing menu toggler script -->
  const toggler = document.querySelector('.navbar-toggler');
  const navMenu = document.querySelector('.navbar-nav');
  const body = document.body;

  if (toggler && navMenu) {
    toggler.addEventListener('click', () => {
      navMenu.classList.toggle('show');
      body.classList.toggle('menu-active');
    });
  }
  
