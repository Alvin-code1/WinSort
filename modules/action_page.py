from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, 
                                QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, 
                                QProgressBar, QFrame,
                                QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QIcon
from worker import WorkerThread

class ActionPage(QWidget):
    def __init__(self, action_name, main_window):
        super().__init__()
        self._cancel_requested = False
        self.setObjectName('ActionPage')
        self.action_name = action_name
        self.main_window = main_window
        self.verbose = False
        self.cascade = False
        self.worker_thread = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Path superior (inicialmente oculto)
        self.path_display = QLabel("")
        self.path_display.setVisible(False)
        
        # Crear sombra para path display
        path_shadow = QGraphicsDropShadowEffect()
        path_shadow.setBlurRadius(10)
        path_shadow.setXOffset(2)
        path_shadow.setYOffset(2)
        path_shadow.setColor(QColor(138, 43, 226, 120))
        self.path_display.setGraphicsEffect(path_shadow)
        
        # Contenedor para inputs y boton iniciar
        input_container = QFrame()
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)
        
        # Layout horizontal para path y boton iniciar
        path_layout = QHBoxLayout()
        path_layout.setSpacing(15)
        
        # Input de path
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Ingrese la ruta de la carpeta")
        self.path_input.setFixedHeight(50)
        
        # Crear sombra para input de path
        path_input_shadow = QGraphicsDropShadowEffect()
        path_input_shadow.setBlurRadius(10)
        path_input_shadow.setXOffset(2)
        path_input_shadow.setYOffset(2)
        path_input_shadow.setColor(QColor(138, 43, 226, 120))
        self.path_input.setGraphicsEffect(path_input_shadow)
        
        # Boton Iniciar
        self.start_btn = QPushButton("Iniciar")
        self.start_btn.setFixedSize(100, 50)
        self.start_btn.setIcon(QIcon('_internal\\play.svg'))
        self.start_btn.setIconSize(QSize(24,24))
        
        # Crear sombra para boton iniciar
        start_btn_shadow = QGraphicsDropShadowEffect()
        start_btn_shadow.setBlurRadius(10)
        start_btn_shadow.setXOffset(2)
        start_btn_shadow.setYOffset(2)
        start_btn_shadow.setColor(QColor(138, 43, 226, 150))
        self.start_btn.setGraphicsEffect(start_btn_shadow)
        
        self.start_btn.clicked.connect(self.start_action)
        
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.start_btn)
        
        # Input de nombre (solo para busqueda)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del archivo a buscar")
        self.name_input.setFixedHeight(50)
        self.name_input.setStyleSheet(self.path_input.styleSheet())
        self.name_input.setVisible(self.action_name == 'search')
        
        # Crear sombra para input de nombre
        name_input_shadow = QGraphicsDropShadowEffect()
        name_input_shadow.setBlurRadius(10)
        name_input_shadow.setXOffset(2)
        name_input_shadow.setYOffset(2)
        name_input_shadow.setColor(QColor(138, 43, 226, 120))
        self.name_input.setGraphicsEffect(name_input_shadow)
        
        input_layout.addLayout(path_layout)
        input_layout.addWidget(self.name_input)
        input_container.setLayout(input_layout)
        
        # Botones de opciones
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)
        
        self.btn_cascade = self.create_option_button("Busqueda recursiva")
        self.btn_verbose = self.create_option_button("Mostrar registro")
        
        self.btn_cascade.clicked.connect(self.toggle_cascade)
        self.btn_verbose.clicked.connect(self.toggle_verbose)
        
        # Visibilidad segun accion
        self.btn_cascade.setVisible(self.action_name in ['sort', 'unsort'])
        self.btn_verbose.setVisible(self.action_name in ['sort', 'unsort'])
        
        options_layout.addWidget(self.btn_cascade)
        options_layout.addWidget(self.btn_verbose)
        options_layout.addStretch()
        
        # Barra de progreso
        self.progress_label = QLabel("Procesando...")
        self.progress_label.setObjectName('StatusLabel')
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        self.progress_label.setVisible(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        
        self.progress_bar.setVisible(False)
        
        # Crear sombra para barra de progreso
        progress_shadow = QGraphicsDropShadowEffect()
        progress_shadow.setBlurRadius(10)
        progress_shadow.setXOffset(2)
        progress_shadow.setYOffset(2)
        progress_shadow.setColor(QColor(138, 43, 226, 120))
        self.progress_bar.setGraphicsEffect(progress_shadow)

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.clicked.connect(self.cancel_action)
        self.cancel_btn.setVisible(False)
        
        # Area de resultados
        self.output = QTextEdit()
        self.output.setObjectName('OutputBox')
        self.output.setReadOnly(True)
        
        self.output.setVisible(False)
        
        # Crear sombra para area de resultados
        output_shadow = QGraphicsDropShadowEffect()
        output_shadow.setBlurRadius(15)
        output_shadow.setXOffset(3)
        output_shadow.setYOffset(3)
        output_shadow.setColor(QColor(138, 43, 226, 150))
        self.output.setGraphicsEffect(output_shadow)
        
        # Boton Volver
        self.btn_back = QPushButton("Volver")
        self.btn_back.setFixedHeight(60)
        self.btn_back.setFixedWidth(120)
        self.btn_back.setIcon(QIcon('_internal\\return.svg'))
        self.btn_back.setIconSize(QSize(24,24))
        
        # Crear sombra para boton volver
        back_btn_shadow = QGraphicsDropShadowEffect()
        back_btn_shadow.setBlurRadius(10)
        back_btn_shadow.setXOffset(2)
        back_btn_shadow.setYOffset(2)
        back_btn_shadow.setColor(QColor(138, 43, 226, 120))
        self.btn_back.setGraphicsEffect(back_btn_shadow)
        
        self.btn_back.clicked.connect(self.main_window.go_back)
        self.btn_back.setVisible(False)
        
        # Agregar todo al layout
        layout.addWidget(self.path_display)
        layout.addWidget(input_container)
        layout.addLayout(options_layout)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.output)
        layout.addWidget(self.btn_back)
        layout.addWidget(self.cancel_btn)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def create_option_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName('OptionButton')
        btn.setCheckable(True)
        btn.setFixedHeight(40)
        
        # Crear sombra para botones de opcion
        option_shadow = QGraphicsDropShadowEffect()
        option_shadow.setBlurRadius(8)
        option_shadow.setXOffset(2)
        option_shadow.setYOffset(2)
        option_shadow.setColor(QColor(138, 43, 226, 100))
        btn.setGraphicsEffect(option_shadow)
        
        return btn
    def reset_view(self):
        self.path_display.setVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.output.setVisible(False)
        self.output.clear()
        self.btn_back.setVisible(False)

        # Mostrar controles inicales
        self.path_input.setVisible(True)
        self.path_input.clear() # Limpiar contenido

        self.name_input.setVisible(self.action_name == 'search')
        self.name_input.clear()

        self.start_btn.setVisible(True)

        self.btn_cascade.setVisible(self.action_name in ['sort', 'unsort'])
        self.btn_verbose.setVisible(self.action_name in ['sort', 'unsort'])

        self.btn_verbose.setChecked(False)
        self.btn_cascade.setChecked(False)

    def toggle_verbose(self):
        self.verbose = self.btn_verbose.isChecked()

    def toggle_cascade(self):
        self.cascade = self.btn_cascade.isChecked()

    def start_action(self):
        self.output.clear()
        path = self.path_input.text().strip()
        if not path:
            path = 'D:\\'
            
        # Mostrar path en la parte superior
        self.path_display.setText(f"Procesando: {path}")
        self.path_display.setVisible(True)

        self._cancel_requested = False
        self.cancel_btn.setVisible(True)
        
        # Ocultar controles y mostrar progreso
        self.path_input.setVisible(False)
        self.name_input.setVisible(False)
        self.start_btn.setVisible(False)
        self.btn_cascade.setVisible(False)
        self.btn_verbose.setVisible(False)
        self.main_window.sidebar.setVisible(False)
        
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.output.clear()
        self.output.setVisible(False)
        self.btn_back.setVisible(False)
        
        # Crear y ejecutar worker thread
        search_name = self.name_input.text().strip() if self.action_name == 'search' else False
        self.worker_thread = WorkerThread(self.action_name, path, search_name, self.cascade, self.verbose)
        self.worker_thread.finished.connect(self.on_task_finished)
        self.worker_thread.error.connect(self.on_task_error)
        self.worker_thread.output_text = ""
        self.worker_thread.start()

    def on_task_finished(self, output_text):
        self.update_output(output_text)
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait(1000)
            self.worker_thread = None
            

    def on_task_error(self, error_text):
        self.update_output(error_text)
    
    def update_output(self,text):
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.output.setVisible(True)
        self.btn_back.setVisible(True)
        self.output.setPlainText(text)
        self.cancel_btn.setVisible(False)
        self.cancel_btn.setEnabled(True)
        self.cancel_btn.setText('Cancelar')
        self.verbose = False
        self.cascade = False
        self.main_window.sidebar.setVisible(True)
    
    def cancel_action(self):
        if self.worker_thread:
            self.worker_thread.cancel()
        self.output.setVisible(True)
        self.output.setPlainText('Accion cancelada por el usuario!')
        self.output.clear()
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.btn_back.setVisible(True)
        self.cancel_btn.setText('Cancelando...')
        self.cancel_btn.setEnabled(False)
        self.main_window.sidebar.setVisible(True)

        self._cancel_requested = True