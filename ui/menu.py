from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtGui import QIcon

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Menú "Ayuda"
        help_menu = self.addMenu("Ayuda")

        # Acción "Acerca de"
        about_action = QAction(QIcon("assets/icons/info.png"), "Acerca de", self)
        about_action.triggered.connect(parent.show_about_window)  # Conectar a la función en MainWindow
        help_menu.addAction(about_action)
        
        # Menú "Idioma"
        language_menu = self.addMenu("Idioma")

        # Acción "Español"
        spanish_action = QAction(QIcon("assets/icons/es.png"), "Español", self)
        spanish_action.triggered.connect(lambda: parent.update_language("es"))
        language_menu.addAction(spanish_action)

        # Acción "Inglés"
        english_action = QAction(QIcon("assets/icons/en.png"), "English", self)
        english_action.triggered.connect(lambda: parent.update_language("en"))
        language_menu.addAction(english_action)