import sqlite3

conn = sqlite3.connect("agf.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE ferramentas ADD COLUMN emprestado_em TEXT")
    conn.commit()
    print("Coluna 'emprestado_em' adicionada com sucesso.")
except sqlite3.OperationalError as e:
    print("Erro:", e)

conn.close()
