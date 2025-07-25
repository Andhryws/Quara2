function toggleMenu() {
      document.getElementById('sideMenu').classList.toggle('active');
      document.getElementById('overlay').classList.toggle('active');
    }

    function closeMenu() {
      document.getElementById('sideMenu').classList.remove('active');
      document.getElementById('overlay').classList.remove('active');
    }