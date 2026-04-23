from database.conexao import conectar

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            idade INT,
            peso FLOAT,
            altura FLOAT,
            nivel VARCHAR(50),
            objetivo TEXT,
            dias_disponiveis INT,
            lesoes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planos_treino (
            id SERIAL PRIMARY KEY,
            id_usuario INT REFERENCES usuarios(id),
            semana INT,
            conteudo TEXT,
            data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_treino (
            id SERIAL PRIMARY KEY,
            id_usuario INT REFERENCES usuarios(id),
            data_treino DATE,
            tipo_treino VARCHAR(100),
            duracao_min INT,
            distancia_km FLOAT,
            nivel_cansaco INT,
            observacoes TEXT
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabelas criadas com sucesso!")