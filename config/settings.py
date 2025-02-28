import os
import json

# Ruta al archivo de configuración del usuario
USER_SETTINGS_FILE = "config/user_settings.json"

def load_user_settings():
    """Carga las configuraciones del usuario desde un archivo JSON."""
    if os.path.exists(USER_SETTINGS_FILE):
        with open(USER_SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

# Configuraciones predeterminadas
user_settings = load_user_settings()

class AppSettings:
    """Configuración general de la aplicación."""
    APP_NAME = "YDown-AF"
    APP_VERSION = "1.0"
    DEVELOPER = "Albis Fox"
    LICENSE = "MIT License"

class Paths:
    """Rutas de archivos y directorios."""
    ASSETS_DIR = "assets"
    ICONS_DIR = f"{ASSETS_DIR}/icons"
    STYLES_FILE = f"{ASSETS_DIR}/styles.qss"
    DEFAULT_SAVE_PATH = user_settings.get("default_save_path", "./downloads")

class YTDLP:
    """Configuración específica para yt-dlp."""
    MP4_FORMAT = "bestvideo[height<=?{quality}]+bestaudio/best"  # Formato para videos MP4
    MP3_FORMAT = "bestaudio/best"  # Mejor calidad de audio (sin opciones adicionales)

class Network:
    """Configuración de red."""
    TIMEOUT = 30  # Tiempo máximo de espera para solicitudes de red (en segundos)

class UI:
    """Configuración de la interfaz gráfica."""
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    LOGO_ICON = "assets/icons/logo.png"
    THEME = user_settings.get("theme", "dark")  # Tema predeterminado: oscuro
    LANGUAGE = user_settings.get("language", "es")  # Idioma predeterminado: español