import yt_dlp
import os
from pathlib import Path
import threading
import time
import tempfile

class YouTubeDownloader:
    def __init__(self):
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)
        self.last_downloaded_file = None
        self.cookies_file = None
        
    def set_cookies(self, cookies_data=None, browser_name=None):
        """Set cookies from either uploaded data or browser name"""
        if cookies_data:
            # Create a temporary file to store the cookies
            temp_cookie_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_cookie_file.write(cookies_data)
            temp_cookie_file.close()
            self.cookies_file = temp_cookie_file.name
            return True
        elif browser_name:
            # Use cookies from a browser
            self.cookies_file = f"--cookies-from-browser={browser_name}"
            return True
        return False
        
    def get_video_info(self, url):
        """Extract video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        # Add cookies if available
        if self.cookies_file:
            if self.cookies_file.startswith('--cookies-from-browser='):
                browser = self.cookies_file.replace('--cookies-from-browser=', '')
                ydl_opts['cookiesfrombrowser'] = (browser, None, None, None)
            else:
                ydl_opts['cookiefile'] = self.cookies_file
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
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
        
        # Base options
        ydl_opts = {
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,  # Single video, not playlist
            'geo_bypass': True,  # Try to bypass geo-restrictions
            'geo_bypass_country': 'US',  # Use US as default
        }
        
        # Add cookies if available
        if self.cookies_file:
            if self.cookies_file.startswith('--cookies-from-browser='):
                browser = self.cookies_file.replace('--cookies-from-browser=', '')
                ydl_opts['cookiesfrombrowser'] = (browser, None, None, None)
            else:
                ydl_opts['cookiefile'] = self.cookies_file
        
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
            if not self.last_downloaded_file.exists():
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
    
    def cleanup(self):
        """Clean up any temporary files"""
        if self.cookies_file and os.path.exists(self.cookies_file) and not self.cookies_file.startswith('--cookies-from-browser='):
            try:
                os.remove(self.cookies_file)
                self.cookies_file = None
            except:
                pass
    
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
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
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
        
        ydl_opts = {
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }
        
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

    def __del__(self):
        """Destructor to clean up resources"""
        self.cleanup()
