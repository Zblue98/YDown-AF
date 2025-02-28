from yt_dlp import YoutubeDL

def download_video(url, save_path, format="mp4", quality=None, progress_callback=None):
    """
    Descarga un video o audio desde YouTube.
    Args:
        url (str): URL del video.
        save_path (str): Ruta donde se guardará el archivo.
        format (str): Formato deseado ('mp4' o 'mp3').
        quality (str): Altura deseada (ejemplo: '720') o None para MP3.
        progress_callback (function): Función de callback para el progreso.
    """
    # Configuración básica de yt-dlp
    if format == "mp4":
        ydl_opts = {
            'format': f"bestvideo[height<={quality}]+bestaudio/best",
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_callback] if progress_callback else []
        }
    elif format == "mp3":
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'progress_hooks': [progress_callback] if progress_callback else [],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise RuntimeError(f"Error durante la descarga: {str(e)}")