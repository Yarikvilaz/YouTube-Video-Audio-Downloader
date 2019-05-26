from os import makedirs
from pytube import YouTube
from pytube.helpers import safe_filename


def download_youtube_video(url, itag=None, audio_only=False, output_path=None,
                           filename=None, filename_prefix=None,
                           proxies=None, progress_callback=None):

    """
    Скачати відео або аудіо з Youtube
    :param url: Повна URL адреса на YouTube відео
    :type url: str
    :param itag: YouTube Stream ITAG to Download
    :type itag: int
    :param audio_only: Скачати тільки аудіо файл із відео на YouTube
    :type audio_only: bool
    :param output_path: Шлях до файлу папки для виведення.
    :type output_path: str
    :param filename: Перевизначення імені файлу. Не перевищує розширення.
    :type filename: str
    :param proxies: Словник, що містить протокол (ключ) і адресу (значення) для проксі.
    :type proxies: dict
    :return: Назва файлу завантаженого відео / аудіо
    :rtype: str
    """
    if output_path:
        makedirs(output_path, exist_ok=True)
    if 'http' not in url:
        url = 'https://www.youtube.com/watch?v=%s' % url
    if proxies:
        video = YouTube(url, proxies=proxies)
    else:
        video = YouTube(url)
    if progress_callback:
        video.register_on_progress_callback(progress_callback)
    if itag:
        itag = int(itag)
        stream = video.streams.get_by_itag(itag)
    else:
        stream = video.streams.filter(only_audio=audio_only).first()
    print('Download Started: %s' % video.title)
    if filename:
        filename = safe_filename(filename)
    stream.download(output_path=output_path, filename=filename)
    file_type = '.' + stream.mime_type.split('/')[1]
    filename = stream.default_filename if filename is None else filename + file_type
    print('Download Complete! Saved to file: %s' % filename)
    return filename
