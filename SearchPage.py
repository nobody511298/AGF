from PySide2.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QComboBox, QDateEdit, QListWidget, QListWidgetItem
)
from PySide2.QtCore import Qt, QDate
import sqlite3
from PySide2.QtGui import QPixmap
from datetime import datetime


class SearchPage(QWidget):
    def __init__(self, db=None, voltar_callback=None):
        super().__init__()
        self.db = db
        self.voltar_callback = voltar_callback

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("🔍 Nome da ferramenta")

        self.responsavel_input = QLineEdit()
        self.responsavel_input.setPlaceholderText("👤 Responsável")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Todos", "Disponível", "Emprestada"])


        self.resultados = QListWidget()

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("🔍 Buscar ferramentas"))
        form_layout.addWidget(self.nome_input)
        form_layout.addWidget(self.responsavel_input)
        form_layout.addWidget(QLabel("Status"))
        form_layout.addWidget(self.status_combo)





        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.realizar_busca)
        form_layout.addWidget(search_button)

        if self.voltar_callback:
            voltar_button = QPushButton("← Voltar")
            voltar_button.clicked.connect(self.voltar_callback)
            form_layout.addWidget(voltar_button)

        layout.addLayout(form_layout)
        layout.addWidget(QLabel("Resultados"))
        layout.addWidget(self.resultados)

        self.setLayout(layout)

    def realizar_busca(self):
        nome = self.nome_input.text().strip()
        responsavel = self.responsavel_input.text().strip()
        status = self.status_combo.currentText()

        query = """
                SELECT id, nome, responsavel, caminho_img, emprestado_para, data_devolucao, emprestado_em
                FROM ferramentas
                WHERE 1 = 1
                """
        params = []

        if nome:
            query += " AND nome LIKE ?"
            params.append(f"%{nome}%")
        if responsavel:
            query += " AND responsavel LIKE ?"
            params.append(f"%{responsavel}%")
        if status == "Disponível":
            query += " AND emprestado_para IS NULL"
        elif status == "Emprestada":
            query += " AND emprestado_para IS NOT NULL"

        # filtro de data removido

        conn = sqlite3.connect("agf.db")
        cursor = conn.cursor()
        cursor.execute(query, params)

        resultados = cursor.fetchall()
        conn.close()

        self.resultados.clear()

        class Ferramenta:
            def __init__(self, id, nome, responsavel, caminho_img, emprestado_para, data_devolucao, emprestado_em):
                self.id = id
                self.nome = nome
                self.responsavel = responsavel
                self.caminho_img = caminho_img
                self.emprestado_para = emprestado_para
                self.data_devolucao = data_devolucao
                self.emprestado_em = emprestado_em
                self.img = QPixmap(caminho_img) if caminho_img else None

        self.ferramentas = []
        for row in resultados:
            f = Ferramenta(*row)
            self.ferramentas.append(f)
            status_text = "🟢 Disponível" if f.emprestado_para is None else f"🔴 Emprestada para {f.emprestado_para} em {f.emprestado_em}"
            item = QListWidgetItem(f"🔧 {f.nome}\n👤 {f.responsavel}\n{status_text}")
            self.resultados.addItem(item)



