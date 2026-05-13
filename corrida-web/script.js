const API = 'http://127.0.0.1:8000';
let usuarioAtual = null;
let idPlanoAtual = null;
let dadosCadastro = {};

window.addEventListener('DOMContentLoaded', function () {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('tela') === 'cadastro') {
    mostrarTela('tela-cadastro');
  }
});

function mostrarTela(id) {
  document.querySelectorAll('.tela').forEach(t => t.classList.remove('ativa'));
  document.getElementById(id).classList.add('ativa');
}

function trocarAba(id, botao) {
  document.querySelectorAll('.aba').forEach(a => a.classList.remove('ativa'));
  document.querySelectorAll('.sidebar-btn').forEach(b => b.classList.remove('ativo'));
  document.getElementById(id).classList.add('ativa');
  botao.classList.add('ativo');
}

function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(email)) { alert('Email invalido!'); return false; }
  const dominios = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com'];
  if (!dominios.includes(email.split('@')[1])) {
    alert('Use um email valido (gmail, hotmail, etc)');
    return false;
  }
  return true;
}

async function verificarEmailExiste(email) {
  try {
    const res = await fetch(`${API}/usuarios/verificar-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await res.json();
    return data.existe;
  } catch { return false; }
}

async function entrar() {
  const email = document.getElementById('input-email').value;
  const senha = document.getElementById('input-senha').value;
  if (!email || !senha) return alert('Preencha email e senha!');

  try {
    const res = await fetch(`${API}/usuarios/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, senha }),
    });
    const dados = await res.json();
    if (!dados.id) throw new Error();

    usuarioAtual = dados;
    mostrarTela('tela-principal');
    document.getElementById('nav-nome').textContent = usuarioAtual.nome;
    document.getElementById('sidebar-inicial').textContent = usuarioAtual.nome.charAt(0).toUpperCase();
  } catch {
    alert('Email ou senha incorretos!');
  }
}

function proximaEtapa(etapaAtual) {
  if (etapaAtual === 1) {
    const nome = document.getElementById('nome').value;
    const idade = document.getElementById('idade').value;
    const peso = document.getElementById('peso').value;
    const altura = document.getElementById('altura').value;
    if (!nome || !idade || !peso || !altura) return alert('Preencha todos os campos!');
    dadosCadastro.nome = nome;
    dadosCadastro.idade = Number(idade);
    dadosCadastro.peso = Number(peso);
    dadosCadastro.altura = Number(altura);
  }
  if (etapaAtual === 2) {
    const objetivo = document.getElementById('objetivo').value;
    const dias = document.getElementById('dias').value;
    if (!objetivo || !dias) return alert('Preencha todos os campos!');
    dadosCadastro.objetivo = objetivo;
    dadosCadastro.dias_disponiveis = Number(dias);
    dadosCadastro.lesoes = document.getElementById('lesoes').value || 'nenhuma';
    dadosCadastro.nivel = document.getElementById('nivel').value;
  }
  document.getElementById(`etapa-${etapaAtual}`).style.display = 'none';
  document.getElementById(`etapa-${etapaAtual + 1}`).style.display = 'block';
  const progresso = ((etapaAtual + 1) / 3) * 100;
  document.getElementById('progresso-fill').style.width = `${progresso}%`;
  document.getElementById('progresso-texto').textContent = `Etapa ${etapaAtual + 1} de 3`;
}

function voltarEtapa(etapaAtual) {
  document.getElementById(`etapa-${etapaAtual + 1}`).style.display = 'none';
  document.getElementById(`etapa-${etapaAtual}`).style.display = 'block';
  const progresso = (etapaAtual / 3) * 100;
  document.getElementById('progresso-fill').style.width = `${progresso}%`;
  document.getElementById('progresso-texto').textContent = `Etapa ${etapaAtual} de 3`;
}

async function cadastrar() {
  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;
  if (!email || !senha) return alert('Preencha email e senha!');
  if (!validarEmail(email)) return;
  const existe = await verificarEmailExiste(email);
  if (existe) { alert('Email ja cadastrado!'); return; }
  dadosCadastro.email = email;
  dadosCadastro.senha = senha;
  try {
    const res = await fetch(`${API}/usuarios/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dadosCadastro),
    });
    if (!res.ok) throw new Error();
    alert('Cadastro realizado! Faca login para continuar.');
    dadosCadastro = {};
    mostrarTela('tela-login');
  } catch { alert('Erro ao cadastrar!'); }
}

function renderizarMarkdown(texto) {
  return texto
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    .replace(/\n/g, '<br>');
}

async function gerarPlano() {
  const div = document.getElementById('resultado-plano');
  div.innerHTML = '<p class="placeholder-text">Gerando seu plano, aguarde...</p>';
  const provedor = document.getElementById('seletor-ia').value;
  try {
    const res = await fetch(`${API}/treinos/plano/${usuarioAtual.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provedor })
    });
    const resultado = await res.json();
    idPlanoAtual = resultado.id_plano;
    await buscarPlanoCompleto(resultado.id_plano);
  } catch {
    div.innerHTML = '<p class="placeholder-text">Erro ao gerar plano.</p>';
  }
}

async function buscarPlanoCompleto(idPlano) {
  const div = document.getElementById('resultado-plano');
  try {
    const res = await fetch(`${API}/treinos/plano-conteudo/${idPlano}`);
    const resultado = await res.json();
    div.innerHTML = renderizarMarkdown(resultado.conteudo);
  } catch {
    div.innerHTML = '<p class="placeholder-text">Erro ao buscar conteudo.</p>';
  }
}

async function ajustarPlano() {
  const div = document.getElementById('resultado-plano');
  div.innerHTML = '<p class="placeholder-text">Ajustando plano com base no historico...</p>';
  const provedor = document.getElementById('seletor-ia').value;
  try {
    const res = await fetch(`${API}/treinos/ajustar/${usuarioAtual.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provedor })
    });
    const resultado = await res.json();
    idPlanoAtual = resultado.id_plano;
    await buscarPlanoCompleto(resultado.id_plano);
  } catch {
    div.innerHTML = '<p class="placeholder-text">Erro ao ajustar plano.</p>';
  }
}

async function salvarTreino() {
  if (!idPlanoAtual) return alert('Gere um plano primeiro!');
  const dados = {
    id_usuario: usuarioAtual.id,
    id_plano: idPlanoAtual,
    data_treino: document.getElementById('data-treino').value,
    tipo_treino: document.getElementById('tipo-treino').value,
    duracao_min: Number(document.getElementById('duracao').value),
    distancia_km: Number(document.getElementById('distancia').value),
    nivel_cansaco: Number(document.getElementById('cansaco').value),
    observacoes: document.getElementById('observacoes').value || 'nenhuma',
  };
  if (!dados.data_treino || !dados.tipo_treino) return alert('Preencha todos os campos!');
  try {
    await fetch(`${API}/treinos/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados),
    });
    alert('Treino registrado com sucesso!');
  } catch { alert('Erro ao salvar treino!'); }
}

async function carregarHistorico() {
  const div = document.getElementById('lista-historico');
  div.innerHTML = '<p class="mensagem">Carregando...</p>';
  try {
    const res = await fetch(`${API}/treinos/historico/${usuarioAtual.id}`);
    const sessoes = await res.json();
    if (sessoes.length === 0) {
      div.innerHTML = '<p class="mensagem">Nenhum treino registrado ainda.</p>';
      return;
    }
    div.innerHTML = sessoes.map(s => `
      <div class="treino-card">
        <h3>${s.tipo}</h3>
        <p>${s.data} &nbsp;|&nbsp; ${s.duracao_min} min &nbsp;|&nbsp; ${s.distancia_km} km &nbsp;|&nbsp; Cansaco: ${s.nivel_cansaco}/10</p>
        ${s.observacoes !== 'nenhuma' ? `<p>${s.observacoes}</p>` : ''}
      </div>
    `).join('');
  } catch {
    div.innerHTML = '<p class="mensagem">Erro ao carregar historico.</p>';
  }
}

function carregarPerfil() {
  if (!usuarioAtual) return;
  document.getElementById('perfil-nome').value     = usuarioAtual.nome             || '';
  document.getElementById('perfil-idade').value    = usuarioAtual.idade            || '';
  document.getElementById('perfil-peso').value     = usuarioAtual.peso             || '';
  document.getElementById('perfil-altura').value   = usuarioAtual.altura           || '';
  document.getElementById('perfil-objetivo').value = usuarioAtual.objetivo         || '';
  document.getElementById('perfil-dias').value     = usuarioAtual.dias_disponiveis || '';
  document.getElementById('perfil-lesoes').value   = usuarioAtual.lesoes           || '';
  document.getElementById('perfil-nivel').value    = usuarioAtual.nivel            || 'iniciante';
}

async function salvarPerfil() {
  const dados = {
    nome:             document.getElementById('perfil-nome').value,
    idade:            Number(document.getElementById('perfil-idade').value),
    peso:             Number(document.getElementById('perfil-peso').value),
    altura:           Number(document.getElementById('perfil-altura').value),
    objetivo:         document.getElementById('perfil-objetivo').value,
    dias_disponiveis: Number(document.getElementById('perfil-dias').value),
    lesoes:           document.getElementById('perfil-lesoes').value || 'nenhuma',
    nivel:            document.getElementById('perfil-nivel').value,
  };
  try {
    const res = await fetch(`${API}/usuarios/${usuarioAtual.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dados)
    });
    if (!res.ok) throw new Error();
    Object.assign(usuarioAtual, dados);
    document.getElementById('nav-nome').textContent = dados.nome;
    document.getElementById('sidebar-inicial').textContent = dados.nome.charAt(0).toUpperCase();
    alert('Perfil atualizado!');
  } catch { alert('Erro ao salvar perfil!'); }
}