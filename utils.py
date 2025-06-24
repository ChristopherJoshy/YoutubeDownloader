import re
import os
from pathlib import Path

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return youtube_regex.match(url) is not None

def format_duration(seconds):
    """Convert seconds to human-readable duration"""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def get_file_size(file_path):
    """Get human-readable file size"""
    try:
        size = os.path.getsize(file_path)
        
        # Convert bytes to human readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "Unknown size"

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    # Remove invalid characters for filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Limit filename length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename.strip()

def get_video_id_from_url(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def format_view_count(count):
    """Format view count to human-readable format"""
    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}B"
    elif count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K"
    else:
        return str(count)

def is_playlist_url(url):
    """Check if URL is a playlist URL"""
    return 'playlist' in url or 'list=' in url

def create_download_directory():
    """Create downloads directory if it doesn't exist"""
    download_dir = Path("downloads")
    download_dir.mkdir(exist_ok=True)
    return download_dir

def clean_old_downloads(days=7):
    """Clean downloads older than specified days"""
    import time
    
    download_dir = Path("downloads")
    if not download_dir.exists():
        return
    
    current_time = time.time()
    cutoff_time = current_time - (days * 24 * 60 * 60)
    
    for file_path in download_dir.rglob("*"):
        if file_path.is_file():
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    print(f"Deleted old file: {file_path.name}")
                except:
                    pass

def get_supported_formats():
    """Get list of supported download formats"""
    return {
        'video': ['mp4', 'webm', 'mkv', 'avi'],
        'audio': ['mp3', 'aac', 'wav', 'ogg', 'm4a']
    }

def validate_format_quality(format_type, quality):
    """Validate if format and quality combination is valid"""
    if format_type in ['mp4', 'webm']:
        valid_qualities = ['Best Quality', '1080p', '720p', '480p', '360p', '240p']
        return quality in valid_qualities
    elif format_type == 'mp3':
        valid_qualities = ['Best Audio', '320kbps', '256kbps', '192kbps', '128kbps', '96kbps', '64kbps']
        return quality in valid_qualities
    
    return False
