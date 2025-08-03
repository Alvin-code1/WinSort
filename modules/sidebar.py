from PySide6.QtWidgets import QPushButton, QVBoxLayout, QFrame
from PySide6.QtCore import Signal, Signal, QSize, QEvent, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon

class Sidebar(QFrame):
    action_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setMinimumWidth(80)
        animation = QPropertyAnimation(self,b'minimumWidth')
        animation.setDuration(350)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation = animation
        close_animation = QPropertyAnimation(self,b'minimumWidth')
        close_animation.setDuration(800)
        close_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.close_animation = close_animation

        self.installEventFilter(self)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(15)
        
        self.buttons = {
            'sort': self.create_sidebar_button('Ordenar','sort'),
            'search': self.create_sidebar_button('Buscar','search'),
            'unsort': self.create_sidebar_button('Deshacer', 'unsort')
        }
        self.button_map = {v: k for k,v in self.buttons.items()}

        layout.addWidget(self.buttons['sort'])
        layout.addWidget(self.buttons['search'])
        layout.addWidget(self.buttons['unsort'])

        layout.addStretch()
        
        self.setLayout(layout)
        self.setVisible(False)
        
    def create_sidebar_button(self, text, action):
        btn = QPushButton()
        btn.setIcon(QIcon(f'_internal\\{action}.svg'))
        btn.setIconSize(QSize(24,24))
        btn.setToolTip(text)
        btn.setStyleSheet('color: transparent;')
        animation = QPropertyAnimation(btn,b'minimumSize')
        animation.setDuration(350)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        btn.animation = animation
        
        btn.installEventFilter(self)
        btn.clicked.connect(lambda: self.action_selected.emit(action))
        return btn
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter and source in self.button_map:
            anim = source.animation
            anim.setStartValue(QSize(30,30))
            anim.setEndValue(QSize(80,30))
            anim.start()
            source.setText(source.toolTip())
            source.setStyleSheet('color: white;')
        elif event.type() == QEvent.Leave and source in self.button_map:
            anim = source.animation
            anim.setStartValue(QSize(80,30))
            anim.setEndValue(QSize(30,30))
            anim.start()
            source.setText('')
            source.setStyleSheet('color: transparent;')
        elif event.type() == QEvent.Enter and source == self:
            anim = self.animation
            anim.setStartValue(self.minimumWidth())
            anim.setEndValue(160)
            anim.start()
        elif event.type() == QEvent.Leave and source == self:
            anim = self.close_animation
            anim.setStartValue(160)
            anim.setEndValue(80)
            anim.start()
        return super().eventFilter(source, event)