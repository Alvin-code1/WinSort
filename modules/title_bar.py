from PySide6.QtWidgets import QLabel, QHBoxLayout, QFrame

class CustomTitleBar(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_action = ""
        self.init_ui()
        
    def init_ui(self):
        self.setObjectName('TitleBar')
        self.setFixedHeight(60)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        self.name_label = QLabel('<h1>WinSort!')
        self.name_label.setObjectName('MainTitle')
        title = f'by BrainStorm'
        self.title_label = QLabel(title)
        self.title_label.setObjectName('BrandName')
        self.action_label = QLabel("")
        self.action_label.setObjectName('ActionLabel')
        layout.addWidget(self.name_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.action_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def set_action(self, action):
        action_names = {
            'sort': 'Ordenar',
            'search': 'Buscar',
            'unsort': 'Deshacer'
        }
        self.action_label.setText(f" {action_names.get(action, '')}")