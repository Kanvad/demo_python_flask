from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = Path(__file__).parent / "downloads"
DOWNLOAD_FOLDER.mkdir(exist_ok=True)
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 5GB max


def get_video_formats(url, content_type='video'):
    """Extract available formats from YouTube video"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if content_type == 'audio':
                return _extract_audio_formats(info)
            else:
                return _extract_video_formats(info)
                
    except Exception as e:
        logger.error(f"Error extracting formats: {str(e)}")
        return {'error': str(e)}


def _extract_video_formats(info):
    """Extract video info dict - auto select best format"""
    return {
        'title': info.get('title', 'Unknown'),
        'duration': info.get('duration', 0),
        'thumbnail': info.get('thumbnail', ''),
        'formats': {},  # Empty - auto select best
        'content_type': 'video'
    }


def _extract_audio_formats(info):
    """Extract best audio format only"""
    # Use bestaudio format - yt_dlp will automatically select best available
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


def download_media(url, format_id, content_type='video'):
    """Download video or audio from YouTube"""
    try:
        if content_type == 'audio':
            return _download_audio(url, format_id)
        else:
            return _download_video(url, format_id)
            
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return {'success': False, 'error': str(e)}


def _download_audio(url, format_id=None):
    """Download and convert audio to MP3"""
    try:
        # Always use bestaudio for audio downloads, ignore format_id
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(DOWNLOAD_FOLDER / '%(title)s'),
            'quiet': False,
            'no_warnings': False,
            'keepvideo': False,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Starting audio download from: {url}")
            info = ydl.extract_info(url, download=True)
            
            # Get the title and handle special characters
            title = info.get('title', 'download')
            # Remove invalid filename characters
            title = "".join(c for c in title if c not in r'<>:"/\|?*')
            filename = f"{title}.mp3"
            filepath = DOWNLOAD_FOLDER / filename
            
            logger.info(f"Audio download completed: {filepath}")
            
            return {
                'success': True,
                'filename': filename,
                'filepath': str(filepath)
            }
    except Exception as e:
        logger.error(f"Audio download error: {str(e)}")
        raise


def _download_video(url, format_id=None):
    """Download video with best quality and audio, convert to MP4"""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(DOWNLOAD_FOLDER / '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'download')
        filename = f"{title}.mp4"
        
        return {
            'success': True,
            'filename': filename,
            'filepath': str(DOWNLOAD_FOLDER / filename)
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-formats', methods=['POST'])
def get_formats():
    """API: Get available formats for URL"""
    data = request.json
    url = data.get('url', '').strip()
    content_type = data.get('content_type', 'video').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    result = get_video_formats(url, content_type)
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result)


@app.route('/download', methods=['POST'])
def download():
    """API: Download video or audio"""
    data = request.json
    url = data.get('url', '').strip()
    content_type = data.get('content_type', 'video').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    if content_type not in ['video', 'audio']:
        return jsonify({'error': 'Invalid content_type'}), 400
    
    result = download_media(url, None, content_type)
    
    if result.get('success'):
        return jsonify({
            'success': True,
            'message': 'Download completed',
            'filename': result['filename']
        })
    else:
        return jsonify({'success': False, 'error': result.get('error', 'Unknown error')}), 500


@app.route('/download-file/<filename>', methods=['GET'])
def download_file(filename):
    """API: Download saved file"""
    filepath = DOWNLOAD_FOLDER / filename
    
    if not filepath.exists():
        return jsonify({'error': 'File not found'}), 404
    
    try:
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download-thumbnail', methods=['POST'])
def download_thumbnail():
    """API: Download thumbnail from YouTube URL"""
    data = request.json
    url = data.get('url', '').strip()
    title = data.get('title', 'thumbnail').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Get thumbnail URL from YouTube
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            thumbnail_url = info.get('thumbnail', '')
        
        if not thumbnail_url:
            return jsonify({'error': 'No thumbnail found'}), 404
        
        # Download thumbnail
        response = requests.get(thumbnail_url, timeout=10)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download thumbnail'}), 400
        
        # Save thumbnail with safe filename
        safe_title = "".join(c for c in title if c not in r'<>:"/\|?*')
        filename = f"{safe_title}.jpg"
        filepath = DOWNLOAD_FOLDER / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Thumbnail downloaded: {filepath}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': str(filepath)
        })
    
    except Exception as e:
        logger.error(f"Thumbnail download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
