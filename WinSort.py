import sys
import os
from PySide6.QtWidgets import QApplication
from  modules.main import MainWindow
from PySide6.QtGui import QFontDatabase

def load_fonts():
    font_paths = [
        '.modules/_internal/fonts/Mulish-Italic-VariableFont_wght.ttf',
        '.modules/_internal/fonts/Manrope-VariableFont_wght.ttf',
        '.modules/_internal/fonts/Syne-VariableFont_wght.ttf',
        '.modules/_internal/fonts/TitilliumWeb-Italic.ttf',
    ]
    for font in font_paths:
        font_id = QFontDatabase.addApplicationFont(font)
        if font_id == -1:
            print(f'Error cargando fuente {font}')

def resource_path(relative_path):
    if hasattr(sys, '__MEIPASS'):
        return os.path.join(sys.__MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'),relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_fonts()
    app.setStyle('Fusion')  # Estilo más moderno
    with open(resource_path('_internal\\styles.qss'),'r') as f:
        app.setStyleSheet(f.read())
    win = MainWindow()
    win.show()
    sys.exit(app.exec())