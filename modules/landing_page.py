from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QSize, QEvent, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon

class LandingPage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.setObjectName('LandingPage')
        self.switch_callback = switch_callback
        self.animations = {}
        self.close_animations = {}
        self.opacity_animations = {}
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setContentsMargins(50, 100, 50, 100)
        layout.setSpacing(30)

        greeting = QLabel('<h1>Hola, en que puedo ayudarte hoy?')
        greeting.setObjectName('Greeting')
        greeting.setAlignment(Qt.AlignCenter)

        layout.addWidget(greeting, 1, 0, 1, 3)
        
        self.buttons = {
            'sort': self.create_main_button('Ordenar','sort'),
            'search': self.create_main_button('Buscar','search'),
            'unsort': self.create_main_button('Deshacer', 'unsort')
        }

        layout.addWidget(self.buttons['sort'], 2, 0)
        layout.addWidget(self.buttons['search'], 2, 1)
        layout.addWidget(self.buttons['unsort'], 2, 2)
        
        self.setLayout(layout)
        
    def create_main_button(self, text, action):
        btn = QPushButton(text)
        animation = QPropertyAnimation(btn,b"minimumSize")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animations[btn] = animation
        close_animation = QPropertyAnimation(btn,b"minimumSize")
        close_animation.setDuration(500)
        close_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.close_animations[btn] = close_animation
        btn.setMinimumSize(QSize(150,150))
        btn.setObjectName(action)
        
        opacity_effect = QGraphicsOpacityEffect(btn)
        opacity_effect.setOpacity(0.85)
        btn.setGraphicsEffect(opacity_effect)
        opacity_anim = QPropertyAnimation(opacity_effect,b'opacity')
        opacity_anim.setDuration(250)
        opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.opacity_animations[btn] = opacity_anim

        btn.setObjectName(self.button_style(normal=True))
        btn.setIcon(QIcon(f'_internal\\{action}.svg'))
        btn.setIconSize(QSize(32,32))

        
        btn.installEventFilter(self)
        btn.clicked.connect(lambda: self.switch_callback(action))
        return btn
    
    def button_style(self, normal=False,focused=False):
        if focused:
            return 'Focused'
        elif normal:
            return 'Normal'
        else:
            return 'Else'
    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter and source in self.buttons.values():
            for btn in self.buttons.values():
                anim = self.animations.get(btn)
                opacity_anim = self.opacity_animations.get(btn)
                if btn is source:
                    btn.setStyleSheet(self.button_style(focused=True))
                    anim.stop()
                    anim.setStartValue(btn.minimumSize())
                    anim.setEndValue(QSize(180,180))
                    anim.start()
                    opacity_anim.stop()
                    opacity_anim.setStartValue(btn.graphicsEffect().opacity())
                    opacity_anim.setEndValue(1.0)
                    opacity_anim.start()
                else:
                    btn.setStyleSheet(self.button_style())
                    anim.stop()
                    anim.setStartValue(btn.minimumSize())
                    anim.setEndValue(QSize(130,130))
                    anim.start()
                    opacity_anim.stop()
                    opacity_anim.setStartValue(btn.graphicsEffect().opacity())
                    opacity_anim.setEndValue(0.6)
                    opacity_anim.start()
        elif event.type() == QEvent.Leave and source in self.buttons.values():
            for btn in self.buttons.values():
                anim = self.close_animations.get(btn)
                opacity_anim = self.opacity_animations.get(btn)
                btn.setStyleSheet(self.button_style(normal=True))
                anim.stop()
                anim.setStartValue(btn.minimumSize())
                anim.setEndValue(QSize(150,150))
                anim.start()
                opacity_anim.stop()
                opacity_anim.setStartValue(btn.graphicsEffect().opacity())
                opacity_anim.setEndValue(0.85)
                opacity_anim.start()
        return super().eventFilter(source, event)
