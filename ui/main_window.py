from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, Qt
from core.scanner import scan_video
from core.downloader import download_video
from ui.menu import MenuBar  # Importamos el menú desde menu.py
from ui.about_window import AboutWindow  # Importamos la ventana de información
from config.settings import AppSettings, Paths, UI
from utils import load_translations  # Importamos la función para cargar traducciones

class MainWindow(QMainWindow):
    def __init__(self, language="es"):
        super().__init__()
        self.language = language  # Idioma seleccionado
        self.translations = load_translations(self.language)  # Cargar traducciones

        self.setWindowTitle(AppSettings.APP_NAME)
        self.setGeometry(100, 100, UI.WINDOW_WIDTH, UI.WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(UI.LOGO_ICON))

        # Cargar el archivo de estilos
        self.load_styles()

        # Inicializar atributos
        self.video_info = None
        self.save_path = Paths.DEFAULT_SAVE_PATH  # Carpeta predeterminada
        self.selected_format = "mp4"  # Formato predeterminado
        self.available_qualities = []

        # Configurar la interfaz gráfica
        self.init_ui()

    def init_ui(self):
        """Configura la interfaz gráfica."""
        # Agregar el menú
        self.setMenuBar(MenuBar(self))  # Instanciar y agregar el menú

        # Layout principal
        layout = QVBoxLayout()

        # Campo de entrada para la URL
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText(self.translations.get("scan_button", "Scan Video"))
        layout.addWidget(self.url_input)

        # Botón para escanear el video
        self.scan_button = QPushButton(self)
        self.scan_button.setIcon(QIcon("assets/icons/scan.png"))  # Ícono de escaneo
        self.scan_button.setText(self.translations.get("scan_button", "Scan Video"))
        self.scan_button.setIconSize(self.scan_button.sizeHint())  # Ajustar tamaño del ícono
        self.scan_button.clicked.connect(self.scan_video_info)
        layout.addWidget(self.scan_button)

        # Etiqueta para mostrar información del video
        self.info_label = QLabel(self.translations.get("video_info", "Video information will appear here"), self)
        layout.addWidget(self.info_label)

        # Contenedor horizontal para la miniatura (centrada)
        thumbnail_layout = QHBoxLayout()
        thumbnail_layout.addStretch()  # Espacio flexible a la izquierda
        self.thumbnail_label = QLabel(self.translations.get("loading_thumbnail", "Loading thumbnail..."), self)
        self.thumbnail_label.setStyleSheet("border: none;")  # Eliminar bordes
        self.thumbnail_label.setFixedSize(200, 150)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        thumbnail_layout.addWidget(self.thumbnail_label)
        thumbnail_layout.addStretch()  # Espacio flexible a la derecha
        layout.addLayout(thumbnail_layout)

        # Contenedor horizontal para formato y calidad
        format_quality_layout = QHBoxLayout()
        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["MP4 (Video)", "MP3 (Audio)"])
        self.format_combo.currentIndexChanged.connect(self.update_format_and_qualities)
        format_quality_layout.addWidget(self.format_combo)

        self.quality_combo = QComboBox(self)
        format_quality_layout.addWidget(self.quality_combo)
        layout.addLayout(format_quality_layout)

        # Botón para seleccionar carpeta de descarga
        self.folder_button = QPushButton(self)
        self.folder_button.setIcon(QIcon("assets/icons/folder.png"))  # Ícono de carpeta
        self.folder_button.setText(self.translations.get("select_folder", "Select Download Folder"))
        self.folder_button.setIconSize(self.folder_button.sizeHint())  # Ajustar tamaño del ícono
        self.folder_button.clicked.connect(self.select_save_folder)
        layout.addWidget(self.folder_button)

        # Etiqueta para mostrar la carpeta seleccionada
        self.folder_label = QLabel(self.translations.get("folder_not_selected", "Download folder not selected"), self)
        self.folder_label.setStyleSheet("color: gray;")
        layout.addWidget(self.folder_label)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Botón para iniciar la descarga
        self.download_button = QPushButton(self)
        self.download_button.setIcon(QIcon("assets/icons/download.png"))  # Ícono de descarga
        self.download_button.setText(self.translations.get("download_button", "Download"))
        self.download_button.setIconSize(self.download_button.sizeHint())  # Ajustar tamaño del ícono
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        # Configurar el widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Gestor de red para descargar miniaturas
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.on_thumbnail_download_finished)

    def update_language(self, language):
        """
        Actualiza el idioma de la aplicación.
        Args:
            language (str): Código del idioma ('es', 'en', etc.).
        """
        self.language = language
        self.translations = load_translations(self.language)  # Recargar traducciones
        self.init_ui()  # Reconstruir la interfaz con el nuevo idioma
        self.show()  # Mostrar la ventana actualizada
    def load_styles(self):
        """Carga el archivo de estilos (styles.qss)."""
        try:
            with open(Paths.STYLES_FILE, "r") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error al cargar los estilos: {str(e)}")

    def show_about_window(self):
        """Muestra la ventana de información."""
        about_window = AboutWindow(self)  # Crear una instancia de la ventana de información
        about_window.exec_()  # Mostrar la ventana como modal

    def update_format_and_qualities(self):
        """Actualiza las opciones de calidad cuando se cambia el formato."""
        if not self.video_info:
            return

        format_text = self.format_combo.currentText()
        self.selected_format = "mp4" if format_text == "MP4 (Video)" else "mp3"

        if self.selected_format == "mp4":
            self.available_qualities = self.video_info['mp4_formats']
            self.quality_combo.setVisible(True)  # Mostrar selector de calidad para MP4
        elif self.selected_format == "mp3":
            self.available_qualities = []  # No hay opciones de calidad para MP3
            self.quality_combo.setVisible(False)  # Ocultar selector de calidad para MP3

        self.quality_combo.clear()
        self.quality_combo.addItems(self.available_qualities)

    def select_save_folder(self):
        """Abre un diálogo para seleccionar la carpeta de descarga."""
        self.save_path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de descarga")
        if self.save_path:
            self.folder_label.setText(f"Carpeta seleccionada: {self.save_path}")
            self.folder_label.setStyleSheet("color: black;")
        else:
            self.folder_label.setText("Carpeta de descarga no seleccionada")
            self.folder_label.setStyleSheet("color: gray;")

    def scan_video_info(self):
        """Escanea el video y muestra su información."""
        url = self.url_input.text()
        try:
            self.video_info = scan_video(url)

            # Formatear la duración
            duration = self.video_info['duration']
            formatted_duration = self.format_duration(duration)

            self.info_label.setText(f"Título: {self.video_info['title']}\nDuración: {formatted_duration}")

            # Mostrar la miniatura
            thumbnail_url = self.video_info['thumbnail']
            if thumbnail_url:
                self.thumbnail_label.setText("Cargando miniatura...")
                self.network_manager.get(QNetworkRequest(QUrl(thumbnail_url)))
            else:
                self.thumbnail_label.setText("Miniatura no disponible")

            # Actualizar las opciones de calidad
            self.update_format_and_qualities()
        except Exception as e:
            self.show_message(f"Error al escanear el video: {str(e)}", "error")

    def on_thumbnail_download_finished(self, reply):
        """Maneja la respuesta de la solicitud de descarga de la miniatura."""
        if reply.error():
            self.thumbnail_label.setText("No se pudo cargar la miniatura")
            return

        # Leer los datos de la respuesta
        data = reply.readAll()
        pixmap = QPixmap()
        if pixmap.loadFromData(data):
            self.thumbnail_label.setPixmap(pixmap.scaled(self.thumbnail_label.size()))
        else:
            self.thumbnail_label.setText("No se pudo cargar la miniatura")

    def download_video(self):
        """Inicia la descarga del video."""
        if not self.save_path:
            self.show_message("Por favor, selecciona una carpeta de descarga.", "error")
            return

        url = self.url_input.text()
        selected_quality = self.quality_combo.currentText()

        try:
            # Extraer la altura de la calidad seleccionada
            height = None
            for part in selected_quality.split():
                if "x" in part:  # Buscar el formato "WIDTHxHEIGHT"
                    height = part.split("x")[1]  # Extraer la altura (segunda parte)
                    break

            if not height and self.selected_format == "mp4":
                raise ValueError("No se pudo extraer la altura de la calidad seleccionada.")

            # Pasar la altura como filtro de calidad
            download_video(
                url=url,
                save_path=self.save_path,
                format=self.selected_format,
                quality=height,  # Solo pasamos la altura para MP4
                progress_callback=self.progress_callback
            )
        except Exception as e:
            self.show_message(f"Error al descargar: {str(e)}", "error")

    def progress_callback(self, data):
        """
        Callback para actualizar la barra de progreso.
        Args:
            data (dict): Datos enviados por yt-dlp.
        """
        status = data.get('status')
        if status == 'downloading':
            downloaded = data.get('downloaded_bytes', 0)
            total = data.get('total_bytes', 1) or data.get('total_bytes_estimate', 1)
            progress = int(downloaded / total * 100)
            self.progress_bar.setValue(progress)
        elif status == 'finished':
            self.show_message("¡Descarga completada!", "success")
        elif status == 'error':
            self.show_message("Ocurrió un error durante la descarga.", "error")

    def format_duration(self, seconds):
        """Formatea la duración en segundos a un formato legible."""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        else:
            return f"{minutes}m {seconds}s"

    def show_message(self, message, message_type="info"):
        """
        Muestra un mensaje usando QMessageBox.
        Args:
            message (str): El mensaje a mostrar.
            message_type (str): El tipo de mensaje ('info', 'error', 'success').
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Notificación")
        msg_box.setText(message)

        if message_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        elif message_type == "success":
            msg_box.setIcon(QMessageBox.Information)
        else:
            msg_box.setIcon(QMessageBox.Information)

        msg_box.exec_()