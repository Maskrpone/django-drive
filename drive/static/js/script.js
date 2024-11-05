// Afficher le menu pour le bouton "+"
document.querySelector('.new-button').addEventListener('click', function() {
  document.querySelector('.add-menu').style.display = 'block';
});

// Fermer le menu "+" en cliquant ailleurs
document.addEventListener('click', function(e) {
  if (!e.target.closest('.new-button') && !e.target.closest('.add-menu')) {
    document.querySelector('.add-menu').style.display = 'none';
  }
});

// Ouverture du modal
document.querySelectorAll('.add-menu ul li').forEach(item => {
  item.addEventListener('click', function() {
    document.getElementById('modal-background').style.display = 'flex';
  });
});

// Fermeture du modal en cliquant sur le fond
document.getElementById('modal-background').addEventListener('click', function(e) {
  if (e.target.id === 'modal-background') {
    document.getElementById('modal-background').style.display = 'none';
  }
});
