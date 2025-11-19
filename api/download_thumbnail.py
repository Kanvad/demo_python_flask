import json
import base64
import tempfile
import os
import requests
from yt_dlp import YoutubeDL

def handler(request):
    if request.method != 'POST':
        return {'statusCode': 405, 'body': 'Method not allowed'}

    data = json.loads(request.body)
    url = data.get('url', '').strip()
    title = data.get('title', 'thumbnail').strip()

    if not url:
        return {'statusCode': 400, 'body': json.dumps({'error': 'URL is required'})}

    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            thumbnail_url = info.get('thumbnail', '')
        
        if not thumbnail_url:
            return {'statusCode': 404, 'body': json.dumps({'error': 'No thumbnail found'})}
        
        response = requests.get(thumbnail_url, timeout=10)
        if response.status_code != 200:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Failed to download thumbnail'})}
        
        safe_title = "".join(c for c in title if c not in r'<>:"/\|?*')
        filename = f"{safe_title}.jpg"
        
        file_data = response.content
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/jpeg',
                'Content-Disposition': f'attachment; filename="{filename}"'
            },
            'body': base64.b64encode(file_data).decode('utf-8'),
            'isBase64Encoded': True
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})} 