from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal

class ClickableFrame(QFrame):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class HomePage(QWidget):
    ferramenta_clicked = Signal(object)  # vai emitir o objeto ferramenta

    def __init__(self, db):
        super().__init__()

        self.db = db

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_layout)

        self.scroll_area.setWidget(self.container_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.load_ferramentas()  # carrega a primeira vez

    def load_ferramentas(self):
        # limpa a lista atual
        for i in reversed(range(self.container_layout.count())):
            widget_to_remove = self.container_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        # cria a lista nova
        for ferramenta in self.db.get_ferramentas():

            container = ClickableFrame()
            container.setStyleSheet("""
                QFrame {
                    border: 1px solid #aaa;
                    border-radius: 6px;
                    padding: 10px;
                    background-color: #f9f9f9;
                    margin-bottom: 10px;
                }
                QFrame:hover {
                    background-color: #e0e0e0;
                    cursor: pointer;
                }
            """)

            layout_f = QHBoxLayout()

            if ferramenta.img and not ferramenta.img.isNull():
                img_label = QLabel()
                pixmap = ferramenta.img.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label.setPixmap(pixmap)
                img_label.setFixedSize(125, 150)
                layout_f.addWidget(img_label)
            else:
                spacer = QLabel()
                spacer.setFixedWidth(70)
                layout_f.addWidget(spacer)

            text_layout = QVBoxLayout()
            nome_label = QLabel(f"🔧 Nome: {ferramenta.nome}")
            responsavel_label = QLabel(f"👤 Responsável: {ferramenta.responsavel}")

            if ferramenta.emprestada:
                status_label = QLabel(f"🚫 Emprestada desde: {ferramenta.emprestado_em}")
                status_label.setStyleSheet("color: red; font-weight: bold;")
            else:
                status_label = QLabel("✅ Disponível")
                status_label.setStyleSheet("color: green; font-weight: bold;")

            text_layout.addWidget(nome_label)
            text_layout.addWidget(responsavel_label)
            text_layout.addWidget(status_label)

            layout_f.addLayout(text_layout)

            container.setLayout(layout_f)
            self.container_layout.addWidget(container)

            # Função pra "congelar" o valor correto de ferramenta
            def make_emit(f):
                return lambda: self.ferramenta_clicked.emit(f)

            container.clicked.connect(make_emit(ferramenta))
