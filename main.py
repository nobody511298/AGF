import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from LoginPage import LoginPage
from About import About
from DBManager import DBManager

from HomePage import HomePage
from ToolPage import ToolPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = DBManager()

        self.setWindowTitle("AGF - Gerenciamento de Ferramentas")
        self.resize(800, 600)  # tamanho inicial, redimensionável e maximizável

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self.login_success)
        self.homepage = HomePage(self.db)
        self.homepage.ferramenta_clicked.connect(self.show_toolpage)  # conecta o clique da ferramenta

        # Passa o callback para voltar e para alterar status da ferramenta
        self.toolpage = ToolPage(
            voltar_callback=self.on_toolpage_voltar,
            alterar_status_callback=self.alterar_status_ferramenta
        )

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.homepage)  # index 1
        self.stack.addWidget(self.toolpage)  # index 2

        self.stack.setCurrentIndex(0)

    def login_success(self, nome_digitado, senha_digitada):
        if self.db.autenticar(nome_digitado, senha_digitada):
            self.stack.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")

    def show_toolpage(self, ferramenta):
        self.toolpage.update_info(ferramenta)
        self.stack.setCurrentIndex(2)

    def show_homepage(self):
        self.stack.setCurrentIndex(1)

    def alterar_status_ferramenta(self, ferramenta):
        # Atualiza o banco conforme o status da ferramenta
        if ferramenta.emprestado_para:
            self.db.emprestar_ferramenta(ferramenta.nome, ferramenta.emprestado_para)
            # Atualiza a data também (supondo que seu DBManager tenha esse método)
            if hasattr(self.db, 'atualizar_data_emprestimo'):
                self.db.atualizar_data_emprestimo(ferramenta.nome, ferramenta.data_emprestimo)
        else:
            self.db.devolver_ferramenta(ferramenta.nome)

    def refresh_homepage(self):
        self.homepage.load_ferramentas()

    def on_toolpage_voltar(self):
        self.homepage.load_ferramentas()
        self.show_homepage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
