from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de YouTube Downloader")
        self.setGeometry(200, 200, 500, 400)  # Tamaño de la ventana
        self.setModal(True)  # Hacer la ventana modal (bloquea la ventana principal mientras está abierta)

        # Configurar la interfaz gráfica
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica."""
        layout = QVBoxLayout()

        # Logo de la aplicación
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Información básica de la aplicación
        info_label = QLabel(
            "<b>YDown-AF</b><br>"
            "Versión: v1.0<br>"
            "Descripción: Una aplicación moderna para descargar videos y audios de YouTube.<br><br>"
            "Desarrollador:<br>"
            "- Nombre: Albis Fox<br>"
            "- GitHub: <a href='https://github.com/Zblue98'>Zblue98</a><br>"
            "- Correo: alvis2100@gmail.com<br><br>"
            "Créditos:<br>"
            "- Bibliotecas utilizadas: yt-dlp, PyQt5.<br>"
            "- Íconos: Descargados de <a href='https://www.flaticon.com/'>Flaticon</a>.<br><br>"
            "Agradecimientos:<br>"
            "- Gracias a la comunidad de PyQt5 por su increíble documentación.<br>"
            "- Gracias a mis amigos y colegas por sus valiosos comentarios."
        )
        info_label.setTextFormat(Qt.RichText)  # Habilitar texto enriquecido (HTML)
        info_label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Permitir interacción con enlaces
        info_label.setOpenExternalLinks(True)  # Abrir enlaces en el navegador
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Segoe UI", 12))  # Fuente moderna
        layout.addWidget(info_label)

        # Botón para cerrar la ventana
        close_button = QPushButton("Cerrar", self)
        close_button.setObjectName("close_button")  # Asignar un nombre de objeto para estilizar
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Configurar el layout
        self.setLayout(layout)