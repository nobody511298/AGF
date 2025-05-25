import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from LoginPage import LoginPage
from DBManager import DBManager
from HomePage import HomePage
from ToolPage import ToolPage
from SearchPage import SearchPage
from AddToolPage import AddToolPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = DBManager()

        self.setWindowTitle("AGF - Aplicativo Gerenciador de Ferramentas")
        self.resize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self.login_success)

        self.homepage = HomePage(self.db)
        self.homepage.ferramenta_clicked.connect(self.show_toolpage)
        self.homepage.abrir_busca_clicked.connect(lambda: self.stack.setCurrentWidget(self.search_page))
        self.homepage.abrir_add_tool_clicked.connect(self.mostrar_add_tool)

        self.search_page = SearchPage(self.db, voltar_callback=self.show_homepage)

        self.toolpage = ToolPage(
            voltar_callback=self.on_toolpage_voltar,
            alterar_status_callback=self.alterar_status_ferramenta
        )

        # Passa só o voltar_callback para AddToolPage
        self.add_tool_page = AddToolPage(
            db=self.db,
            voltar_callback=self.show_homepage,
            refresh_callback=self.refresh_homepage
        )

        self.stack.addWidget(self.login_page)      # index 0
        self.stack.addWidget(self.homepage)        # index 1
        self.stack.addWidget(self.toolpage)        # index 2
        self.stack.addWidget(self.search_page)     # index 3
        self.stack.addWidget(self.add_tool_page)   # index 4

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
        self.refresh_homepage()
        self.stack.setCurrentIndex(1)

    def mostrar_add_tool(self):
        self.stack.setCurrentWidget(self.add_tool_page)

    def alterar_status_ferramenta(self, ferramenta):
        if ferramenta.emprestado_para:
            self.db.emprestar_ferramenta(ferramenta.nome, ferramenta.emprestado_para)
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
