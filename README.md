# WinSort by BrainStorm

![Icono](modules/_internal/icono.ico)

WinSort es una aplicacion de escritorio desarrollada con **Python** y **PySide6**, 
diseñado para ayudarte a **ordenar**, **buscar** y **deshacer** cambios en directorios y archivos. 
Su interfaz elegante y moderna proporciona una experiencia amigable para el usuario.

---

## Características

    - Interfaz gráfica moderna y personalizable.
    - Botones con íconos y animaciones fluidas.
    - Funcionalidades para:
        - Enumerar archivos de manera recursiva (incluyendo carpetas interiores)
        - Ordenar ficheros .srt y agruparlos en una carpeta interior.
        - Renombrar archivos que se encuentren dentro de directorios de Series o Animes
        para organizarlos más facil ([Nombre de la serie] "Episodio" [numero del episodio].[extension])
        - Deshacer enumeraciones
        - Buscar el path de un fichero dentro de un directorio especifico o en todo el volumen (default)
    - Modo detallado con registros (verbose)
    - Barra lateral animada
    - Barra superior personalizada
    - Fondos decorativos

---

## Tecnologias Usadas

- **Python 3.13**
- **PySide6**
-  **QThread / QPropertyAnimation / QGraphicsEffect**
- **QSS (Qt StyleSheet)**
- **SVG y fondos personalizados**

---

## Como Ejecutar

1. Instalar las dependencias
    
    ```bash
    pip install -r requirements.txt
    ```

2. Ejeutar la aplicacion

    ```bash
    py WinSort.py
    ```

---

Compilar Ejecutable

Usa PyInstaller:

    ```bash
    pyinstaller --windowed --icon=modiles/_internal/icono.ico --add-data='modiles/_internal/styles.qss;.' --add-data='modiles/_internal/background.png;.' --add-data='modiles/_internal/icono.png;.' --add-data='modiles/_internal/play.svg;.' --add-data='modiles/_internal/return.svg;.' --add-data='modiles/_internal/search.svg;.' --add-data='modiles/_internal/sort.svg;.' --add-data='modiles/_internal/unsort.svg;.' --add-data='icono.ico;.' --add-data='modiles/_internal/fonts;fonts' WinSort.py
    ```

---

## Estructura del Proyecto

    winSort /
    |--- WinSort.py
    |--- README.md
    |___ modules/
            |--- action_page.py
            |--- landing_page.py
            |--- main.py
            |--- sidebar.py
            |--- sort.py
            |--- title_bar.py
            |--- worker.py
            |___ _internal/
                    |--- background.png
                    |--- icono.ico
                    |--- icono.png
                    |--- play.svg
                    |--- return.svg
                    |--- sort.svg
                    |--- styles.qss
                    |--- unsort.svg
                    |___ fonts/
                            |___ ....