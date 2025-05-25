from PySide2.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QInputDialog, QMessageBox
)
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, QDateTime, QDate
import re
from datetime import datetime


class ToolPage(QWidget):
    def __init__(self, voltar_callback=None, alterar_status_callback=None):
        super().__init__()

        self.voltar_callback = voltar_callback
        self.alterar_status_callback = alterar_status_callback  # callback para avisar alteração

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.img_label = QLabel()
        self.nome_label = QLabel()
        self.responsavel_label = QLabel()
        self.status_label = QLabel()

        self.status_button = QPushButton()
        self.status_button.setFixedWidth(140)
        self.status_button.setFixedHeight(30)
        self.status_button.clicked.connect(self._on_status_button_clicked)

        self.voltar_button = QPushButton("← Voltar")
        self.voltar_button.setFixedWidth(80)
        self.voltar_button.setFixedHeight(25)
        if self.voltar_callback:
            self.voltar_button.clicked.connect(self.voltar_callback)

        self.layout.addWidget(self.img_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.nome_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.responsavel_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.status_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.voltar_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        self.ferramenta_atual = None

    def update_info(self, ferramenta):
        self.ferramenta_atual = ferramenta

        if hasattr(ferramenta, 'img') and ferramenta.img and not ferramenta.img.isNull():
            pixmap = ferramenta.img.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.img_label.setPixmap(pixmap)
        else:
            self.img_label.clear()

        self.nome_label.setText(f"🔧 Nome: {ferramenta.nome}")
        self.responsavel_label.setText(f"👤 Responsável: {ferramenta.responsavel}")

        if hasattr(ferramenta, 'emprestado_para') and ferramenta.emprestado_para:
            status_text = (f"Status: 🔴 Emprestada para {ferramenta.emprestado_para}\n"
                           f"Data Empréstimo: {ferramenta.emprestado_em or 'não informada'}")
            if hasattr(ferramenta, 'data_devolucao') and ferramenta.data_devolucao:
                status_text += f"\nData Devolução: {ferramenta.data_devolucao}"
            self.status_label.setText(status_text)
            self.status_button.setText("Devolver Ferramenta")
            self.status_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px;")
        else:
            self.status_label.setText("Status: 🟢 Disponível")
            self.status_button.setText("Emprestar Ferramenta")
            self.status_button.setStyleSheet("background-color: #4caf50; color: white; border-radius: 5px;")

    def _on_status_button_clicked(self):
        if not self.ferramenta_atual:
            return

        if self.ferramenta_atual.emprestado_para:
            # Devolver ferramenta
            resposta = QMessageBox.question(
                self, "Confirmar devolução",
                f"Deseja devolver a ferramenta '{self.ferramenta_atual.nome}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if resposta == QMessageBox.Yes:
                self.ferramenta_atual.emprestado_para = None
                self.ferramenta_atual.emprestado_em = None
                self.ferramenta_atual.data_devolucao = None

                if self.alterar_status_callback:
                    self.alterar_status_callback(self.ferramenta_atual)
                self.update_info(self.ferramenta_atual)

        else:
            # Emprestar ferramenta: só pede nome e data de devolução válida
            funcionario, ok1 = QInputDialog.getText(self, "Emprestar Ferramenta", "Informe o nome do funcionário:")
            if not ok1 or not funcionario.strip():
                return

            while True:
                data_devolucao, ok2 = QInputDialog.getText(
                    self, "Data de Devolução",
                    "Informe a data prevista para devolução (ex: 18/05/2025):"
                )
                if not ok2 or not data_devolucao.strip():
                    return

                texto = data_devolucao.strip()

                # valida formato dd/mm/aaaa
                if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", texto):
                    QMessageBox.warning(self, "Formato inválido", "Use o formato DD/MM/AAAA.")
                    continue

                try:
                    dia, mes, ano = map(int, texto.split("/"))
                    data = QDate(ano, mes, dia)
                    if not data.isValid():
                        raise ValueError()

                    if data < QDate.currentDate():
                        QMessageBox.warning(self, "Data inválida", "A data não pode ser anterior ao dia atual.")
                        continue
                except:
                    QMessageBox.warning(self, "Erro", "Data inválida.")
                    continue

                break  # data válida

            self.ferramenta_atual.emprestado_para = funcionario.strip()
            self.ferramenta_atual.emprestado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.ferramenta_atual.data_devolucao = data_devolucao.strip()

            if self.alterar_status_callback:
                self.alterar_status_callback(self.ferramenta_atual)
            self.update_info(self.ferramenta_atual)
