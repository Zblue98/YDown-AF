import json
import os

def load_translations(language="es"):
    """
    Carga las traducciones para el idioma especificado.
    Args:
        language (str): Código del idioma ('es', 'en', etc.).
    Returns:
        dict: Diccionario con las traducciones.
    """
    translations_file = f"translations/{language}.json"
    if os.path.exists(translations_file):
        with open(translations_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"No se encontró el archivo de traducción para el idioma '{language}'.")