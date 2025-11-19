import json
import base64
import tempfile
import os
from yt_dlp import YoutubeDL

def handler(request):
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method not allowed'}

    data = json.loads(request.body)
    url = data.get('url', '').strip()
    content_type = data.get('content_type', 'video').strip()

    if not url:
        return {'statusCode': 400, 'body': json.dumps({'error': 'URL is required'})}

    if content_type not in ['video', 'audio']:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid content_type'})}

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            if content_type == 'audio':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(tmpdir, '%(title)s'),
                    'quiet': False,
                    'no_warnings': False,
                    'keepvideo': False,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'download')
                    title = "".join(c for c in title if c not in r'<>:"/\|?*')
                    filename = f"{title}.mp3"
                    filepath = os.path.join(tmpdir, filename)
                    with open(filepath, 'rb') as f:
                        file_data = f.read()
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'audio/mpeg',
                            'Content-Disposition': f'attachment; filename="{filename}"'
                        },
                        'body': base64.b64encode(file_data).decode('utf-8'),
                        'isBase64Encoded': True
                    }
            else:
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'quiet': False,
                    'no_warnings': False,
                    'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferredformat': 'mp4'
                }],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'download')
                    filename = f"{title}.mp4"
                    filepath = os.path.join(tmpdir, filename)
                    with open(filepath, 'rb') as f:
                        file_data = f.read()
                    return {
                        'statusCode': 200,
                        'headers': {
                            'Content-Type': 'video/mp4',
                            'Content-Disposition': f'attachment; filename="{filename}"'
                        },
                        'body': base64.b64encode(file_data).decode('utf-8'),
                        'isBase64Encoded': True
                    }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'success': False, 'error': str(e)})} 