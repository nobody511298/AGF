from PySide2.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QSizePolicy
)
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt



class AddToolPage(QWidget):
    def __init__(self, db, voltar_callback=None, refresh_callback=None):
        super().__init__()
        self.db = db
        self.voltar_callback = voltar_callback
        self.refresh_callback = refresh_callback

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 40, 50, 40)

        # Título
        titulo = QLabel("Adicionar Nova Ferramenta")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setStyleSheet("color: #333333")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Campo: Nome da ferramenta
        layout.addLayout(self._criar_campo("Nome da ferramenta", 'nome_input'))

        # Campo: Responsável
        layout.addLayout(self._criar_campo("Responsável", 'responsavel_input'))

        # Campo: Caminho da imagem
        img_layout = QVBoxLayout()
        lbl_img = QLabel("Caminho da imagem")
        lbl_img.setFont(QFont("Arial", 10))
        img_layout.addWidget(lbl_img)

        caminho_layout = QHBoxLayout()
        self.caminho_img_input = QLineEdit()
        self.caminho_img_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        caminho_layout.addWidget(self.caminho_img_input)

        btn_browse = QPushButton("Selecionar...")
        btn_browse.clicked.connect(self.selecionar_imagem)
        caminho_layout.addWidget(btn_browse)

        img_layout.addLayout(caminho_layout)
        layout.addLayout(img_layout)

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_salvar = QPushButton("Salvar")
        btn_salvar.setStyleSheet("padding: 6px 20px; background-color: #4CAF50; color: white;")
        btn_salvar.clicked.connect(self.salvar_ferramenta)
        btn_layout.addWidget(btn_salvar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("padding: 6px 20px; background-color: #f44336; color: white;")
        btn_cancelar.clicked.connect(self.voltar_callback or self.close)
        btn_layout.addWidget(btn_cancelar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _criar_campo(self, label_text, attr_name):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 10))
        layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setMinimumHeight(30)
        layout.addWidget(line_edit)

        setattr(self, attr_name, line_edit)
        return layout

    def selecionar_imagem(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecione a imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)")
        if caminho:
            self.caminho_img_input.setText(caminho)

    def salvar_ferramenta(self):
        nome = self.nome_input.text().strip()
        responsavel = self.responsavel_input.text().strip()
        caminho_img = self.caminho_img_input.text().strip()

        if not nome or not responsavel:
            QMessageBox.warning(self, "Erro", "Nome e Responsável são obrigatórios.")
            return

        sucesso = self.db.adicionar_ferramenta(nome, responsavel, caminho_img)

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Ferramenta adicionada com sucesso!")
            if self.voltar_callback:
                self.voltar_callback()
        else:
            QMessageBox.critical(self, "Erro", "Erro ao salvar ferramenta no banco de dados.")
