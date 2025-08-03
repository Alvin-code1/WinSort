from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon
from title_bar import CustomTitleBar
from sidebar import Sidebar
from landing_page import LandingPage
from action_page import ActionPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinSort")
        self.setWindowIcon(QIcon('_internal\\icono.ico'))
        self.setFixedSize(900, 700)
        self.setStyleSheet("QMainWindow { background-image: url('_internal//background.png'); background-repeat: repeat; background-position: 100%;}")
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de título personalizada
        self.title_bar = CustomTitleBar(self)
        self.title_bar.setVisible(False)
        main_layout.addWidget(self.title_bar)
        
        # Contenedor para sidebar y contenido
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.setObjectName('Sidebar')
        self.sidebar.action_selected.connect(self.switch_view)
        content_layout.addWidget(self.sidebar)
        
        # Stack de páginas
        self.stack = QStackedWidget()
        self.landing_page = LandingPage(self.switch_view)
        self.stack.addWidget(self.landing_page)
        content_layout.addWidget(self.stack)
        
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        central_widget.setLayout(main_layout)
        
        self.pages = {}

    def switch_view(self, action):
        # Mostrar sidebar y actualizar título
        self.sidebar.setVisible(True)
        self.title_bar.setVisible(True)
        self.title_bar.set_action(action)
        
        # Crear o mostrar página de acción
        if action not in self.pages:
            self.pages[action] = ActionPage(action, self)
            self.stack.addWidget(self.pages[action])

        # Resetear la vista antes de mostrarla
        self.pages[action].reset_view()
        self.stack.setCurrentWidget(self.pages[action])

    def go_back(self):
        for page in self.pages.values():
            if hasattr(page, 'worker_thread') and page.worker_thread:
                page.worker_thread.quit()
                page.worker_thread.wait()
                page.worker_thread = None
        # Volver a landing page y ocultar sidebar
        self.sidebar.setVisible(False)
        self.title_bar.setVisible(False)
        self.title_bar.set_action("")
        self.stack.setCurrentWidget(self.landing_page)