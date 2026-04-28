// Redireciona para a tela certa no index.html
const params = new URLSearchParams(window.location.search);
const tela = params.get('tela');

if (tela === 'cadastro') {
  window.location.href = 'index.html?tela=cadastro';
}