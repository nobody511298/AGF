import sqlite3

#configurar DB


conn = sqlite3.connect("agf.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ferramenta_id INTEGER,
    nome_ferramenta TEXT,
    responsavel TEXT,
    acao TEXT,  -- 'emprestimo' ou 'devolucao'
    data_hora TEXT  --  "2025-05-23 14:12"
);
""")

conn.commit()
conn.close()
