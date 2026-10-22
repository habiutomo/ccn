const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.nav-links');

menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  navigation?.classList.toggle('is-open', !open);
});

navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  navigation.classList.remove('is-open');
  menuButton?.setAttribute('aria-expanded', 'false');
}));
