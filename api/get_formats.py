import json
from yt_dlp import YoutubeDL

def handler(request):
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method not allowed'}

    data = json.loads(request.body)
    url = data.get('url', '').strip()
    content_type = data.get('content_type', 'video').strip()

    if not url:
        return {'statusCode': 400, 'body': json.dumps({'error': 'URL is required'})}

    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if content_type == 'audio':
                result = _extract_audio_formats(info)
            else:
                result = _extract_video_formats(info)
        return {'statusCode': 200, 'body': json.dumps(result)}
    except Exception as e:
        return {'statusCode': 400, 'body': json.dumps({'error': str(e)})}

def _extract_video_formats(info):
    return {
        'title': info.get('title', 'Unknown'),
        'duration': info.get('duration', 0),
        'thumbnail': info.get('thumbnail', ''),
        'formats': {},
        'content_type': 'video'
    }

def _extract_audio_formats(info):
    best_format = {
        'bestaudio/best': {
            'quality': 'Best Available Audio',
            'bitrate': 0,
            'size': 0
        }
    }
    return {
        'title': info.get('title', 'Unknown'),
        'duration': info.get('duration', 0),
        'thumbnail': info.get('thumbnail', ''),
        'formats': best_format,
        'content_type': 'audio'
    }