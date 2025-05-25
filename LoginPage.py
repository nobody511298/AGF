from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QPainter, QPainterPath


class LoginPage(QWidget):
    def __init__(self, login_callback):
        super().__init__()

        self.login_callback = login_callback

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)

        login_box = QVBoxLayout()
        login_box.setSpacing(15)

        logo_label = QLabel()
        pixmap = QPixmap("Archives/img_login.png")
        if pixmap.isNull():
            print("Erro: imagem não encontrada")
        else:
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = self.rounded_pixmap(pixmap, radius=15)
            logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Título principal
        title_label = QLabel("Login do Sistema")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")

        # Aviso de uso restrito
        warning_label = QLabel(
            "⚠️Este aplicativo é exclusivo para fins acadêmicos.")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("""
            font-size: 11px;
            color: #b71c1c;
            padding: 6px;
            border: 1px solid #e57373;
            background-color: #ffebee;
            border-radius: 6px;
        """)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuário")
        self.user_input.setFixedHeight(35)
        self.user_input.setStyleSheet("padding: 5px;")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Senha")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedHeight(35)
        self.pass_input.setStyleSheet("padding: 5px;")

        login_button = QPushButton("Entrar")
        login_button.setFixedHeight(35)
        login_button.clicked.connect(self.handle_login)
        login_button.setStyleSheet("""
            background-color: #3498db;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        """)

        login_box.addWidget(logo_label)
        login_box.addWidget(title_label)
        login_box.addWidget(warning_label)
        login_box.addWidget(self.user_input)
        login_box.addWidget(self.pass_input)
        login_box.addWidget(login_button)

        container = QWidget()
        container.setLayout(login_box)
        container.setFixedWidth(300)

        outer_layout.addWidget(container)
        self.setLayout(outer_layout)

    def rounded_pixmap(self, pixmap, radius=15):
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return rounded

    def handle_login(self):
        usuario = self.user_input.text()
        senha = self.pass_input.text()
        self.login_callback(usuario, senha)
