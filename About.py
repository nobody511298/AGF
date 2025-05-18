from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout

class About(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("Bem-vindo à página Sobre")
        layout.addWidget(label)
        self.setLayout(layout)
