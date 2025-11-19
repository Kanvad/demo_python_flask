# YouTube Video Downloader

[![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A modern Flask web application for downloading YouTube videos and audio with quality selection. Features a beautiful, responsive UI with dark mode and multi-language support.

![App Screenshot](https://via.placeholder.com/800x400?text=YouTube+Downloader+Screenshot)

## Features

- 🎬 Download videos from YouTube in various qualities
- 🎵 Extract audio as MP3
- 🎯 Automatic quality selection for best experience
- 📊 Display video information (title, duration, thumbnail)
- 🚀 Simple and intuitive web interface
- 🌙 Dark mode support
- 🌐 Multi-language support (English/Vietnamese)
- 📱 Responsive design for mobile devices
- ⚡ Fast and reliable downloads using yt-dlp
- 🖼️ Download video thumbnails
- 📈 Download progress indicators

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- FFmpeg (for audio conversion)

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Kanvad/flask_youtube_downloader.git
    cd flask_youtube_downloader
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install FFmpeg (required for audio conversion):**
    - **Ubuntu/Debian:** `sudo apt install ffmpeg`
    - **macOS:** `brew install ffmpeg`
    - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

1. **Start the Flask application:**
    ```bash
    python app.py
    ```

2. **Open your browser:**
    Navigate to `http://localhost:5000`

3. **Download content:**
    - Paste a YouTube URL
    - Choose download type (Video or Audio)
    - Click "Get Video Info" to load details
    - Click "Download Video/Music" or "Download Thumbnail"

### Interface Features

- **Language Toggle:** Switch between English and Vietnamese
- **Dark Mode:** Toggle between light and dark themes
- **Progress Bar:** Visual download progress indicator
- **Responsive Design:** Works on desktop and mobile devices

## API Documentation

The application provides REST API endpoints for programmatic access:

### GET `/`
Returns the main web interface.

### POST `/get-formats`
Get video/audio information and available formats.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "content_type": "video" | "audio"
}
```

**Response:**
```json
{
  "title": "Video Title",
  "duration": 3600,
  "thumbnail": "https://...",
  "formats": {...},
  "content_type": "video"
}
```

### POST `/download`
Download video or audio.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "content_type": "video" | "audio"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Download completed",
  "filename": "video.mp4"
}
```

### POST `/download-thumbnail`
Download video thumbnail.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "Video Title"
}
```

### GET `/download-file/<filename>`
Download the saved file.

## File Structure

```
flask_youtube_downloader/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web interface with modern UI
├── downloads/               # Downloaded files (created automatically)
├── .gitignore              # Git ignore rules
├── README.md               # This documentation
└── flask_youtube_downloader.iml  # PyCharm project file
```

## How It Works

1. **URL Processing**: yt-dlp extracts video metadata and available formats
2. **Format Selection**: Automatically selects best quality for video, best audio for MP3
3. **Download**: Downloads content using yt-dlp with FFmpeg for conversion
4. **File Serving**: Provides download links for completed files

## Supported Formats

- **Video**: MP4 (H.264 + AAC) - automatically selects best available quality
- **Audio**: MP3 (192kbps) - extracts from best available audio stream
- **Thumbnail**: JPG - high quality thumbnail download

## Local Development

```bash
python app.py
# Access at http://localhost:5000
```



## Troubleshooting

### Common Issues

**"No formats found"**
- Video URL is invalid or video is private/restricted
- Try a different video or check URL format

**"Download failed"**
- Network issues or YouTube restrictions
- Check internet connection and try again

**"FFmpeg not found"**
- Install FFmpeg as described in prerequisites
- Ensure it's in your system PATH

**"File not found after download"**
- Check `downloads/` folder permissions
- Ensure sufficient disk space

### Performance Tips
- Downloads are faster with better internet connection
- Audio extraction is quicker than video downloads
- Clear downloads folder periodically to free space

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature"`
5. Push to your branch: `git push origin feature-name`
6. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Ensure responsive design works on mobile

## Changelog

### v1.1.0 (Current)
- Added dark mode toggle
- Multi-language support (English/Vietnamese)
- Download progress indicators
- Improved accessibility with ARIA labels
- Enhanced UI with modern design
- Added thumbnail download feature

### v1.0.0
- Initial release
- Basic YouTube video/audio download
- Flask web interface
- Responsive design

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- **Framework:** [Flask](https://flask.palletsprojects.com/) - Web framework
- **Downloader:** [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- **Icons:** [Font Awesome](https://fontawesome.com/) - UI icons
- **Styling:** Modern CSS with gradients and animations

## Disclaimer

This tool is for educational purposes only. Downloading copyrighted content may violate YouTube's Terms of Service and local laws. Users are responsible for ensuring their use complies with applicable regulations.
