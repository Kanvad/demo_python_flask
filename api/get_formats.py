import json
from yt_dlp import YoutubeDL

def handler(request):
    # Simple test response
    result = {
        'title': 'Test Video',
        'duration': 120,
        'thumbnail': 'https://via.placeholder.com/120x120',
        'formats': {},
        'content_type': 'video'
    }
    return {'statusCode': 200, 'body': json.dumps(result)}

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