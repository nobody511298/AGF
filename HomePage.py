from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QPushButton
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal

class ClickableFrame(QFrame):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class HomePage(QWidget):
    ferramenta_clicked = Signal(object)
    abrir_busca_clicked = Signal()
    abrir_add_tool_clicked = Signal()


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

        # layout dos botões superiores
        botoes_layout = QHBoxLayout()
        botoes_layout.setAlignment(Qt.AlignLeft)

        search_button = QPushButton("🔍 Buscar ferramentas")
        search_button.setFixedHeight(30)
        search_button.setStyleSheet("background-color: #1976d2; color: white; border-radius: 6px;")
        search_button.clicked.connect(self.abrir_busca_clicked.emit)
        botoes_layout.addWidget(search_button)

        add_tool_button = QPushButton("➕ Adicionar ferramenta")
        add_tool_button.setFixedHeight(30)
        add_tool_button.setStyleSheet("background-color: #388e3c; color: white; border-radius: 6px; margin-left: 8px;")
        add_tool_button.clicked.connect(self.abrir_add_tool_clicked.emit)
        botoes_layout.addWidget(add_tool_button)



        main_layout.addLayout(botoes_layout)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.load_ferramentas()

    def load_ferramentas(self):
        for i in reversed(range(self.container_layout.count())):
            widget_to_remove = self.container_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

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

            def make_emit(f):
                return lambda: self.ferramenta_clicked.emit(f)

            container.clicked.connect(make_emit(ferramenta))
