from yt_dlp import YoutubeDL

def scan_video(url):
    """
    Escanea un video de YouTube y devuelve información relevante.
    Args:
        url (str): URL del video.
    Returns:
        dict: Información del video, incluyendo formatos disponibles.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'forceurl': False
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Filtrar formatos MP4 (video)
        # core/scanner.py
        mp4_formats = [
            f"{format['resolution']} ({format['ext']})"
            for format in info.get('formats', [])
            if format.get('ext') == 'mp4' and format.get('vcodec') != 'none'
        ]

        # Filtrar formatos MP3 (audio)
       # core/scanner.py
        mp3_formats = [
            f"{format['abr']}kbps ({format['ext']})"
            for format in info.get('formats', [])
            if format.get('ext') == 'm4a' and format.get('acodec') != 'none'
        ]

        return {
            'title': info.get('title', 'Sin título'),
            'duration': info.get('duration', 0),
            'thumbnail': info.get('thumbnail', ''),
            'mp4_formats': list(set(mp4_formats)),  # Eliminar duplicados
            'mp3_formats': list(set(mp3_formats))  # Eliminar duplicados
        }