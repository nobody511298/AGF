import sqlite3
from PySide2.QtGui import QPixmap
from datetime import datetime

class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

class Ferramenta:
    def __init__(self, nome, responsavel, caminho_img=None):
        self.nome = nome
        self.responsavel = responsavel
        self.emprestado_para = None
        self.emprestado_em = None
        self.img = None

        if caminho_img:
            self.img = QPixmap(caminho_img)

    @property
    def emprestada(self):
        return bool(self.emprestado_para)


class DBManager:
    def __init__(self, db_path="agf.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # acessar colunas por nome
        self.cursor = self.conn.cursor()

    def autenticar(self, nome, senha):
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha)
        )
        return self.cursor.fetchone() is not None

    def get_usuarios(self):
        self.cursor.execute("SELECT * FROM usuarios")
        return [Usuario(row["nome"], row["senha"]) for row in self.cursor.fetchall()]

    def get_ferramentas(self):
        self.cursor.execute(
            "SELECT nome, responsavel, caminho_img, emprestado_para, emprestado_em FROM ferramentas"
        )
        ferramentas = []
        for row in self.cursor.fetchall():
            ferramenta = Ferramenta(
                row["nome"],
                row["responsavel"],
                row["caminho_img"],
            )
            ferramenta.emprestado_para = row["emprestado_para"]
            ferramenta.emprestado_em = row["emprestado_em"]
            ferramentas.append(ferramenta)
        return ferramentas

    def emprestar_ferramenta(self, nome_ferramenta, funcionario):
        emprestado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            """
            UPDATE ferramentas
            SET emprestado_para = ?, emprestado_em = ?
            WHERE nome = ? AND (emprestado_para IS NULL OR emprestado_para = '')
            """,
            (funcionario, emprestado_em, nome_ferramenta),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0  # True se atualizou algo

    def devolver_ferramenta(self, nome_ferramenta):
        self.cursor.execute(
            """
            UPDATE ferramentas
            SET emprestado_para = NULL, emprestado_em = NULL
            WHERE nome = ? AND (emprestado_para IS NOT NULL AND emprestado_para != '')
            """,
            (nome_ferramenta,),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.conn.close()

    def adicionar_ferramenta(self, nome, responsavel, caminho_img):
        try:
            conn = sqlite3.connect("agf.db")
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO ferramentas (nome, responsavel, caminho_img, emprestado_para, data_devolucao,
                                                    emprestado_em)
                           VALUES (?, ?, ?, NULL, NULL, NULL)
                           """, (nome, responsavel, caminho_img))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao adicionar ferramenta: {e}")
            return False

    def buscar_ferramentas(self, termo):
        termo_like = f"%{termo}%"
        query = """
            SELECT id, nome, responsavel, caminho_img, emprestado_para, data_devolucao, emprestado_em
            FROM ferramentas
            WHERE nome LIKE ?
               OR responsavel LIKE ?
               OR emprestado_para LIKE ?
               OR data_devolucao LIKE ?
               OR emprestado_em LIKE ?
        """
        self.cursor.execute(query, (termo_like, termo_like, termo_like, termo_like, termo_like))
        rows = self.cursor.fetchall()

        ferramentas = []
        for row in rows:
            ferramenta = {
                "id": row[0],
                "nome": row[1],
                "responsavel": row[2],
                "caminho_img": row[3],
                "emprestado_para": row[4],
                "data_devolucao": row[5],
                "emprestado_em": row[6],
            }
            ferramentas.append(ferramenta)
        return ferramentas
