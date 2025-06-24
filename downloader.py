import yt_dlp
import os
import random
from pathlib import Path
import threading
import time

class YouTubeDownloader:
    def __init__(self):
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)
        self.last_downloaded_file = None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Edge/124.0.0.0'
        ]
        
    def _get_base_options(self):
        """Get base options with anti-bot detection measures"""
        # Select a random user agent
        user_agent = random.choice(self.user_agents)
        
        return {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_color': True,
            'geo_bypass': True,
            'extractor_retries': 3,
            'socket_timeout': 20,
            'http_headers': {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.youtube.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers'
            }
        }
        
    def get_video_info(self, url):
        """Extract video information without downloading"""
        ydl_opts = self._get_base_options()
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    return None
                
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'uploader': info.get('uploader', 'Unknown Channel'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'id': info.get('id', ''),
                    'formats': info.get('formats', [])
                }
        except Exception as e:
            print(f"Error extracting video info: {str(e)}")
            return None
    
    def download_video(self, url, format_type='mp4', quality='Best Quality', progress_callback=None):
        """Download video with specified format and quality"""
        
        # Ensure downloads directory exists
        self.download_dir.mkdir(exist_ok=True)
        
        # Configure output template
        output_template = str(self.download_dir / '%(title)s.%(ext)s')
        
        # Base options with anti-bot detection
        ydl_opts = self._get_base_options()
        ydl_opts['outtmpl'] = output_template
        
        # Add additional options to bypass restrictions
        ydl_opts.update({
            'skip_download': False,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 10,
            'retry_sleep_functions': {'fragment': lambda n: 5 * (n + 1)},
            'max_sleep_interval': 30
        })
        
        # Format-specific options
        if format_type == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': self._get_audio_quality(quality),
                }],
            })
        elif format_type == 'mp4':
            if quality == 'Best Quality':
                ydl_opts['format'] = 'best[ext=mp4]/best'
            else:
                height = self._get_video_height(quality)
                ydl_opts['format'] = f'best[height<={height}][ext=mp4]/best[height<={height}]'
        elif format_type == 'webm':
            if quality == 'Best Quality':
                ydl_opts['format'] = 'best[ext=webm]/best'
            else:
                height = self._get_video_height(quality)
                ydl_opts['format'] = f'best[height<={height}][ext=webm]/best[height<={height}]'
        
        # Add progress hook if callback provided
        if progress_callback:
            ydl_opts['progress_hooks'] = [self._progress_hook(progress_callback)]
        
        try:
            # Get file metadata before download to predict filename
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                if info_dict:
                    # Get the title and extension
                    title = info_dict.get('title', 'video')
                    if format_type == 'mp3':
                        ext = 'mp3'
                    else:
                        ext = info_dict.get('ext', format_type)
                    
                    # Sanitize the filename (similar to what yt-dlp does)
                    from utils import sanitize_filename
                    clean_title = sanitize_filename(title)
                    self.last_downloaded_file = self.download_dir / f"{clean_title}.{ext}"
                
            # Now do the actual download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # Verify file exists and find it if the filename is different
            if self.last_downloaded_file and not self.last_downloaded_file.exists():
                # Try to find the most recently created file
                files = list(self.download_dir.glob("*"))
                if files:
                    self.last_downloaded_file = max(files, key=lambda x: x.stat().st_mtime)
                
            return True
        except Exception as e:
            print(f"Download error: {str(e)}")
            self.last_downloaded_file = None
            return False
    
    def get_last_downloaded_file(self):
        """Return the path to the last downloaded file"""
        return self.last_downloaded_file
    
    def delete_file(self, file_path=None):
        """Delete a file from the downloads directory"""
        if file_path is None and self.last_downloaded_file:
            file_path = self.last_downloaded_file
            
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
                if file_path == self.last_downloaded_file:
                    self.last_downloaded_file = None
                return True
            except Exception as e:
                print(f"Error deleting file: {str(e)}")
                return False
        return False
    
    def _get_audio_quality(self, quality):
        """Convert quality string to audio bitrate"""
        quality_map = {
            'Best Audio': '320',
            '128kbps': '128',
            '96kbps': '96',
            '64kbps': '64'
        }
        return quality_map.get(quality, '192')
    
    def _get_video_height(self, quality):
        """Convert quality string to video height"""
        quality_map = {
            '1080p': 1080,
            '720p': 720,
            '480p': 480,
            '360p': 360
        }
        return quality_map.get(quality, 720)
    
    def _progress_hook(self, callback):
        """Create progress hook for yt-dlp"""
        def hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and 'downloaded_bytes' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    callback(progress)
                elif 'total_bytes_estimate' in d and 'downloaded_bytes' in d:
                    progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                    callback(progress)
            elif d['status'] == 'finished':
                callback(100)
        return hook
    
    def get_available_formats(self, url):
        """Get all available formats for a video"""
        try:
            ydl_opts = self._get_base_options()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return {'video_formats': [], 'audio_formats': []}
                    
                formats = info.get('formats', [])
                
                # Filter and organize formats
                video_formats = []
                audio_formats = []
                
                for fmt in formats:
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        # Video with audio
                        video_formats.append({
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'resolution': fmt.get('resolution', 'Unknown'),
                            'filesize': fmt.get('filesize', 0),
                            'fps': fmt.get('fps', 0)
                        })
                    elif fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                        # Audio only
                        audio_formats.append({
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'abr': fmt.get('abr', 0),
                            'filesize': fmt.get('filesize', 0)
                        })
                
                return {
                    'video_formats': video_formats,
                    'audio_formats': audio_formats
                }
        except Exception as e:
            print(f"Error getting formats: {str(e)}")
            return {'video_formats': [], 'audio_formats': []}
    
    def download_playlist(self, url, format_type='mp4', quality='Best Quality', progress_callback=None):
        """Download entire playlist"""
        output_template = str(self.download_dir / '%(playlist_title)s/%(title)s.%(ext)s')
        
        # Get base options with anti-bot measures
        ydl_opts = self._get_base_options()
        ydl_opts['outtmpl'] = output_template
        
        # Add additional options to bypass restrictions
        ydl_opts.update({
            'skip_download': False,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 10
        })
        
        # Configure format same as single video
        if format_type == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': self._get_audio_quality(quality),
                }],
            })
        elif format_type == 'mp4':
            if quality == 'Best Quality':
                ydl_opts['format'] = 'best[ext=mp4]/best'
            else:
                height = self._get_video_height(quality)
                ydl_opts['format'] = f'best[height<={height}][ext=mp4]/best[height<={height}]'
        
        if progress_callback:
            ydl_opts['progress_hooks'] = [self._progress_hook(progress_callback)]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"Playlist download error: {str(e)}")
            return False
