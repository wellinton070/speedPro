const API = 'http://127.0.0.1:8000';
let usuarioAtual = null;
let idPlanoAtual = null;
let dadosCadastro = {};


// Verifica se veio da landing page com tela específica
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('tela') === 'cadastro') {
  mostrarTela('tela-cadastro');
}
// ── Navegação ──────────────────────────────────────────────────────────────

function mostrarTela(id) {
  document.querySelectorAll('.tela').forEach(t => t.classList.remove('ativa'));
  document.getElementById(id).classList.add('ativa');
}

function mostrarAba(id, botao) {
  document.querySelectorAll('.aba').forEach(a => a.classList.remove('ativa'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('ativo'));
  document.getElementById(id).classList.add('ativa');
  botao.classList.add('ativo');
}

// ── Validação de Email ─────────────────────────────────────────────────────

function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!regex.test(email)) {
    alert('Email inválido!');
    return false;
  }

  const dominiosPermitidos = [
    'gmail.com',
    'hotmail.com',
    'outlook.com',
    'yahoo.com'
  ];

  const dominio = email.split('@')[1];

  if (!dominiosPermitidos.includes(dominio)) {
    alert('Use um email válido (gmail, hotmail, etc)');
    return false;
  }

  return true;
}

// ── Verificar Email na API ────────────────────────────────────────────────

async function verificarEmailExiste(email) {
  try {
    const res = await fetch(`${API}/usuarios/verificar-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });

    const data = await res.json();
    return data.existe;
  } catch {
    alert('Erro ao verificar email!');
    return true;
  }
}

// ── Login ──────────────────────────────────────────────────────────────────

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
    document.getElementById('nav-nome').textContent = `Olá, ${usuarioAtual.nome}!`;

  } catch {
    alert('Email ou senha incorretos!');
  }
}

// ── Cadastro ──────────────────────────────────────────────────────────────

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

// 🔥 CADASTRO COM VALIDAÇÃO
async function cadastrar() {
  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;

  if (!email || !senha) return alert('Preencha email e senha!');

  // validar email
  if (!validarEmail(email)) return;

  // verificar duplicado
  const existe = await verificarEmailExiste(email);

  if (existe) {
    alert('Email já cadastrado!');
    return;
  }

  dadosCadastro.email = email;
  dadosCadastro.senha = senha;

  try {
    const res = await fetch(`${API}/usuarios/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dadosCadastro),
    });

    if (!res.ok) throw new Error();

    alert('Cadastro realizado com sucesso! Faça login para continuar.');
    dadosCadastro = {};
    mostrarTela('tela-login');

  } catch {
    alert('Erro ao cadastrar!');
  }
}

// ── Plano de Treino ────────────────────────────────────────────────────────

async function gerarPlano() {
  const div = document.getElementById('resultado-plano');
  div.style.display = 'block';
  div.textContent = 'Gerando seu plano, aguarde...';

  try {
    const res = await fetch(`${API}/treinos/plano/${usuarioAtual.id}`, { method: 'POST' });
    const resultado = await res.json();
    idPlanoAtual = resultado.id_plano;
    await buscarPlanoCompleto(resultado.id_plano);
  } catch {
    div.textContent = 'Erro ao gerar plano!';
  }
}

async function buscarPlanoCompleto(idPlano) {
  const div = document.getElementById('resultado-plano');
  try {
    const res = await fetch(`${API}/treinos/plano-conteudo/${idPlano}`);
    const resultado = await res.json();
    div.textContent = resultado.conteudo;
  } catch {
    div.textContent = 'Erro ao buscar conteúdo do plano!';
  }
}

async function ajustarPlano() {
  const div = document.getElementById('resultado-plano');
  div.style.display = 'block';
  div.textContent = 'Analisando histórico e ajustando plano...';

  try {
    const res = await fetch(`${API}/treinos/ajustar/${usuarioAtual.id}`, { method: 'POST' });
    const resultado = await res.json();
    idPlanoAtual = resultado.id_plano;
    await buscarPlanoCompleto(resultado.id_plano);
  } catch {
    div.textContent = 'Erro ao ajustar plano!';
  }
}

// ── Registrar Treino ───────────────────────────────────────────────────────

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
  } catch {
    alert('Erro ao salvar treino!');
  }
}

// ── Histórico ──────────────────────────────────────────────────────────────

async function carregarHistorico() {
  const div = document.getElementById('lista-historico');
  div.innerHTML = '<p class="mensagem">Carregando...</p>';

  try {
    const res = await fetch(`${API}/treinos/historico/${usuarioAtual.id}`);
    const sessoes = await res.json();

    if (sessoes.length === 0) {
      div.innerHTML = '<p class="mensagem">Nenhum treino registrado ainda!</p>';
      return;
    }

    div.innerHTML = sessoes.map(s => `
      <div class="treino-card">
        <h3>${s.tipo}</h3>
        <p>📅 ${s.data}</p>
        <p>⏱ ${s.duracao_min} min | 📍 ${s.distancia_km} km | 💪 Cansaço: ${s.nivel_cansaco}/10</p>
        ${s.observacoes !== 'nenhuma' ? `<p>📝 ${s.observacoes}</p>` : ''}
      </div>
    `).join('');
  } catch {
    div.innerHTML = '<p class="mensagem">Erro ao carregar histórico!</p>';
  }
}
