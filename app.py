import streamlit as st
import os
import threading
import time
import datetime
import random
from pathlib import Path
import base64
from downloader import YouTubeDownloader
from utils import validate_youtube_url, format_duration, get_file_size

# Page configuration
st.set_page_config(
    page_title="Terminal",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'download_progress' not in st.session_state:
    st.session_state.download_progress = 0
if 'download_status' not in st.session_state:
    st.session_state.download_status = ""
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'downloading' not in st.session_state:
    st.session_state.downloading = False
if 'terminal_logs' not in st.session_state:
    st.session_state.terminal_logs = []
if 'log_counter' not in st.session_state:
    st.session_state.log_counter = 0
if 'current_downloader' not in st.session_state:
    st.session_state.current_downloader = None
if 'file_downloaded' not in st.session_state:
    st.session_state.file_downloaded = False
if 'error_message' not in st.session_state:
    st.session_state.error_message = None
if 'fallback_used' not in st.session_state:
    st.session_state.fallback_used = None
if 'extraction_attempts' not in st.session_state:
    st.session_state.extraction_attempts = 0

# Load custom CSS and JavaScript
def load_hacker_css():
    with open('static/hacker-terminal.css', 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def load_matrix_js():
    with open('static/matrix-rain.js', 'r') as f:
        js = f.read()
    st.components.v1.html(f"""
        <script>{js}</script>
    """, height=0)

# Load hacker terminal styling
load_hacker_css()
load_matrix_js()

# Generate random terminal logs
def add_random_log():
    logs = [
        "Scanning network interfaces...",
        "Bypassing firewall restrictions...",
        "Establishing encrypted tunnel...",
        "Intercepting data packets...",
        "Decrypting video metadata...",
        "Injecting extraction payload...",
        "Spoofing user agent headers...",
        "Masking IP address...",
        "Accessing restricted protocols...",
        "Downloading secure certificates...",
        "Buffer overflow detected - exploiting...",
        "SQL injection attempt successful...",
        "Cross-site scripting payload active...",
        "Privilege escalation in progress...",
        "Memory dump analysis complete...",
        "Keylogger deployment successful...",
        "Port scan initiated on target...",
        "Brute force attack commenced...",
        "Social engineering phase complete...",
        "Zero-day exploit activated...",
        "Rotating user agents...",
        "Proxying connection through nodes...",
        "Bypassing content filters...",
        "Implementing evasion techniques...",
        "Randomizing request patterns..."
    ]
    
    if len(st.session_state.terminal_logs) > 15:
        st.session_state.terminal_logs.pop(0)
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {random.choice(logs)}"
    st.session_state.terminal_logs.append(log_entry)

# Add logs periodically
st.session_state.log_counter += 1
if st.session_state.log_counter % 3 == 0:
    add_random_log()

# Terminal interface
st.markdown("""
<div style="background: #000000; color: #00ff41; font-family: 'Fira Code', monospace; padding: 0; margin: 0;">
    <div style="border-bottom: 1px solid #00ff41; padding: 0.5rem;">
        <span style="color: #00ff41;">root@darkweb:~$ </span><span style="animation: blink 1s infinite;">_</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Show random logs with better spacing
if st.session_state.terminal_logs:
    st.markdown('<div class="command-output" style="margin-bottom: 1rem;">', unsafe_allow_html=True)
    for log in st.session_state.terminal_logs[-6:]:  # Show last 6 logs for better spacing
        st.markdown(f'<div class="command-line" style="margin: 0.1rem 0;">{log}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Command prompt
st.markdown("""
<div style="background: #000000; color: #00ff41; font-family: 'Fira Code', monospace; padding: 0.5rem; border: 1px solid #00ff41;">
    <span style="color: #00aa33;">root@system:~$</span> What do you want to extract?
</div>
""", unsafe_allow_html=True)

# URL input 
url = st.text_input(
    "command",
    placeholder="paste_url_here",
    key="youtube_url",
    label_visibility="collapsed"
)

# Execute button
if st.button("execute", key="fetch_info"):
    if url:
        if validate_youtube_url(url):
            add_random_log()
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Initiating target acquisition...")
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Scanning URL: {url[:50]}...")
            st.session_state.error_message = None
            st.session_state.extraction_attempts = 0
            
            with st.spinner("processing..."):
                downloader = YouTubeDownloader()
                st.session_state.current_downloader = downloader
                try:
                    st.session_state.extraction_attempts += 1
                    video_info = downloader.get_video_info(url)
                    if video_info:
                        st.session_state.video_info = video_info
                        st.session_state.fallback_used = video_info.get('fallback_used', None)
                        if st.session_state.fallback_used:
                            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Using extraction method: {st.session_state.fallback_used}")
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Target acquired - Video metadata extracted")
                        st.rerun()
                    else:
                        st.session_state.error_message = downloader.get_last_error() or "Unknown extraction error"
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Extraction failed - {st.session_state.error_message}")
                        st.rerun()
                except Exception as e:
                    st.session_state.error_message = str(e)
                    st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Error: {str(e)}")
                    st.rerun()
        else:
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Invalid URL format detected")
            st.rerun()
    else:
        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] No input provided")

# Display error message if present
if st.session_state.error_message:
    st.markdown(f"""
    <div style="background: #330000; color: #ff0000; font-family: 'Fira Code', monospace; padding: 0.5rem; border: 1px solid #ff0000; margin: 0.5rem 0;">
        <span style="color: #ff0000;">ERROR:</span> {st.session_state.error_message}
    </div>
    """, unsafe_allow_html=True)
    
    # Provide retry option if extraction failed
    if st.session_state.extraction_attempts < 3:
        if st.button("retry_with_fallback", key="retry_btn"):
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Retrying with alternative extraction methods...")
            st.session_state.extraction_attempts += 1
            
            with st.spinner("processing_fallbacks..."):
                downloader = YouTubeDownloader()
                st.session_state.current_downloader = downloader
                try:
                    video_info = downloader.get_video_info(url)
                    if video_info:
                        st.session_state.video_info = video_info
                        st.session_state.fallback_used = video_info.get('fallback_used', None)
                        if st.session_state.fallback_used:
                            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Using extraction method: {st.session_state.fallback_used}")
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Target acquired - Video metadata extracted")
                        st.session_state.error_message = None
                        st.rerun()
                    else:
                        st.session_state.error_message = downloader.get_last_error() or "Unknown extraction error"
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Fallback extraction failed - {st.session_state.error_message}")
                        st.rerun()
                except Exception as e:
                    st.session_state.error_message = str(e)
                    st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Fallback error: {str(e)}")
                    st.rerun()

# Display video information if available
if st.session_state.video_info:
    video_info = st.session_state.video_info
    
    # Show target data in terminal format with better spacing
    st.markdown('<div class="command-output" style="margin: 1rem 0;">', unsafe_allow_html=True)
    st.markdown(f'<div class="command-line" style="margin: 0.1rem 0;">target_title: {video_info.get("title", "unknown")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="command-line" style="margin: 0.1rem 0;">source_channel: {video_info.get("uploader", "unknown")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="command-line" style="margin: 0.1rem 0;">duration: {format_duration(video_info.get("duration", 0))}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="command-line" style="margin: 0.1rem 0;">view_count: {video_info.get("view_count", "unknown"):,}</div>', unsafe_allow_html=True)
    
    # Show which extraction method was used
    if st.session_state.fallback_used:
        st.markdown(f'<div class="command-line" style="margin: 0.1rem 0; color: #ffcc00;">extraction_method: {st.session_state.fallback_used}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="command-line" style="margin: 0.1rem 0;">status: ready_for_extraction</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Command prompt for format selection
    st.markdown("""
    <div style="background: #000000; color: #00ff41; font-family: 'Fira Code', monospace; padding: 0.5rem; border: 1px solid #00ff41; margin: 0.5rem 0;">
        <span style="color: #00aa33;">root@system:~$</span> select extraction format:
    </div>
    """, unsafe_allow_html=True)
    
    # Format and quality selection with minimal spacing
    col_format, col_quality = st.columns(2)
    
    with col_format:
        format_option = st.selectbox(
            "format",
            ["mp4", "mp3", "webm"],
            key="format_select",
            label_visibility="collapsed"
        )
    
    with col_quality:
        if format_option == "mp3":
            quality_option = st.selectbox(
                "quality",
                ["best", "128k", "96k", "64k"],
                key="quality_select",
                label_visibility="collapsed"
            )
        else:
            quality_option = st.selectbox(
                "resolution",
                ["best", "1080p", "720p", "480p", "360p"],
                key="quality_select",
                label_visibility="collapsed"
            )
    
    # Add spacing
    st.markdown('<div style="margin: 0.5rem 0;"></div>', unsafe_allow_html=True)
    
    # Download button
    if not st.session_state.downloading:
        if st.button("extract", key="download_btn"):
            st.session_state.downloading = True
            st.session_state.download_progress = 0
            st.session_state.download_status = "initializing..."
            st.session_state.error_message = None
            st.session_state.fallback_used = None
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Starting extraction protocol...")
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Format: {format_option} | Quality: {quality_option}")
            
            # Start download in background thread
            def download_video():
                downloader = YouTubeDownloader()
                st.session_state.current_downloader = downloader
                try:
                    # Convert format names
                    format_map = {"mp4": "mp4", "mp3": "mp3", "webm": "webm"}
                    quality_map = {
                        "best": "Best Quality",
                        "128k": "128kbps", "96k": "96kbps", "64k": "64kbps",
                        "1080p": "1080p", "720p": "720p", "480p": "480p", "360p": "360p"
                    }
                    
                    file_format = format_map.get(format_option, "mp4")
                    file_quality = quality_map.get(quality_option, "Best Quality")
                    
                    if hasattr(st.session_state, 'terminal_logs'):
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Injecting payload...")
                    
                    # Download the video
                    success = downloader.download_video(
                        url, 
                        format_type=file_format,
                        quality=file_quality,
                        progress_callback=update_progress
                    )
                    
                    if success:
                        st.session_state.download_status = "extraction_complete"
                        st.session_state.download_progress = 100
                        st.session_state.fallback_used = downloader.get_fallback_used()
                        
                        if hasattr(st.session_state, 'terminal_logs'):
                            if st.session_state.fallback_used:
                                st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Successful extraction using: {st.session_state.fallback_used}")
                            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] File secured in downloads directory")
                            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] File ready for download")
                    else:
                        st.session_state.download_status = "extraction_failed"
                        st.session_state.download_progress = 0
                        st.session_state.error_message = downloader.get_last_error() or "Unknown download error"
                        
                        if hasattr(st.session_state, 'terminal_logs'):
                            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Extraction failed - {st.session_state.error_message}")
                    
                except Exception as e:
                    st.session_state.download_status = f"error: {str(e)}"
                    st.session_state.download_progress = 0
                    st.session_state.error_message = str(e)
                    
                    if hasattr(st.session_state, 'terminal_logs'):
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] System error: {str(e)}")
                
                st.session_state.downloading = False
            
            def update_progress(progress):
                st.session_state.download_progress = progress
                st.session_state.download_status = f"extracting... {progress:.1f}%"
                if progress % 20 == 0 and hasattr(st.session_state, 'terminal_logs'):  # Add log every 20%
                    st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Progress: {progress:.0f}% complete")
            
            # Start download thread
            download_thread = threading.Thread(target=download_video)
            download_thread.daemon = True
            download_thread.start()
    
    # Progress display in terminal format
    if st.session_state.downloading or st.session_state.download_progress > 0:
        st.markdown('<div class="command-output">', unsafe_allow_html=True)
        
        # Terminal progress display
        progress_bar = "█" * int(st.session_state.download_progress // 5) + "░" * (20 - int(st.session_state.download_progress // 5))
        st.markdown(f'<div class="command-line">status: {st.session_state.download_status}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="command-line">progress: [{progress_bar}] {st.session_state.download_progress:.1f}%</div>', unsafe_allow_html=True)
        
        if st.session_state.fallback_used:
            st.markdown(f'<div class="command-line">using: {st.session_state.fallback_used}</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-refresh while downloading
        if st.session_state.downloading:
            time.sleep(0.5)
            st.rerun()
        
        # Show download completion and file info
        if st.session_state.download_progress == 100 and not st.session_state.downloading:
            downloads_dir = Path("downloads")
            if downloads_dir.exists():
                download_files = list(downloads_dir.glob("*"))
                if download_files:
                    latest_file = max(download_files, key=lambda x: x.stat().st_mtime)
                    file_size = get_file_size(latest_file)
                    
                    st.markdown('<div class="command-output" style="margin: 1rem 0;">', unsafe_allow_html=True)
                    st.markdown(f'<div class="command-line">file_saved: {latest_file.name}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="command-line">file_size: {file_size}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="command-line">location: ./downloads/{latest_file.name}</div>', unsafe_allow_html=True)
                    
                    if st.session_state.fallback_used:
                        st.markdown(f'<div class="command-line">extraction_method: {st.session_state.fallback_used}</div>', unsafe_allow_html=True)
                        
                    st.markdown('<div class="command-line" style="color: #ffcc00;">warning: file will be deleted after download</div>', unsafe_allow_html=True)
                    
                    # Provide download button
                    with open(latest_file, "rb") as file:
                        file_data = file.read()
                    
                    if st.download_button(
                        label="download_file",
                        data=file_data,
                        file_name=latest_file.name,
                        mime="application/octet-stream",
                        key="download_file_btn"
                    ):
                        # This code runs after the download button is clicked
                        st.session_state.file_downloaded = True
                        st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] File downloaded - executing cleanup...")
                        
                        # Delete the file
                        if st.session_state.current_downloader:
                            st.session_state.current_downloader.delete_file()
                            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] File {latest_file.name} deleted from server")
                        else:
                            # Fallback if downloader instance is not available
                            try:
                                os.remove(latest_file)
                                st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] File {latest_file.name} deleted from server")
                            except Exception as e:
                                st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Error during cleanup: {str(e)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
    # Display error message if download failed
    if st.session_state.error_message and not st.session_state.downloading and st.session_state.download_progress == 0:
        st.markdown(f"""
        <div style="background: #330000; color: #ff0000; font-family: 'Fira Code', monospace; padding: 0.5rem; border: 1px solid #ff0000; margin: 0.5rem 0;">
            <span style="color: #ff0000;">DOWNLOAD ERROR:</span> {st.session_state.error_message}
        </div>
        """, unsafe_allow_html=True)
        
        # Provide retry option
        if st.button("retry_extraction", key="retry_download_btn"):
            st.session_state.terminal_logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Retrying download with alternate methods...")
            st.session_state.downloading = True
            st.session_state.download_progress = 0
            st.session_state.download_status = "initializing..."
            st.session_state.error_message = None
            
            # Start retry thread
            download_thread = threading.Thread(target=download_video)
            download_thread.daemon = True
            download_thread.start()
            st.rerun()

# Keep adding random logs to simulate activity
if st.session_state.log_counter % 5 == 0:
    add_random_log()

# Auto-refresh to show new logs (reduced frequency)
if len(st.session_state.terminal_logs) > 0 and st.session_state.log_counter % 10 == 0:
    time.sleep(0.5)
    st.rerun()

# Add footer with version and fallback information
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; border-top: 1px solid #00ff41; padding: 5px 10px; font-family: 'Fira Code', monospace; font-size: 12px; color: #00aa33;">
    <span>Terminal YouTube Extractor v0.1.1 | Multiple Extraction Methods | Auto-Cleanup</span>
</div>
""", unsafe_allow_html=True)
