from flask import Flask, request, jsonify, send_from_directory, send_file, after_this_request
import yt_dlp
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="static")

# Use temporary directory for downloads (files will be cleaned up)
TEMP_DIR = os.path.join(tempfile.gettempdir(), "instagram_downloader")
os.makedirs(TEMP_DIR, exist_ok=True)


def detect_platform(url):
    """Detect the platform from the URL."""
    url_lower = url.lower()
    if "instagram.com" in url_lower:
        return "instagram"
    elif "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    else:
        return None


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL requerida"}), 400

    # Detect platform for display purposes
    platform = detect_platform(url)
    if platform is None:
        return jsonify({"error": "Plataforma no soportada. Usa Instagram o YouTube."}), 400

    platform_name = "Instagram" if platform == "instagram" else "YouTube"

    # Generate a unique filename for temporary storage
    import uuid
    temp_filename = f"temp_{uuid.uuid4().hex}"
    
    # Check for cookies from environment variable or file
    cookies_file = "/app/cookies.txt"
    cookies_env = os.environ.get("YOUTUBE_COOKIES", "")
    cookies_base64 = os.environ.get("COOKIES_BASE64", "")
    
    logger.info(f"Environment variable YOUTUBE_COOKIES exists: {bool(cookies_env)}")
    logger.info(f"Environment variable COOKIES_BASE64 exists: {bool(cookies_base64)}")
    
    # Create cookies file from base64 if provided
    if cookies_base64:
        try:
            import base64
            cookies_content = base64.b64decode(cookies_base64).decode('utf-8')
            with open(cookies_file, "w") as f:
                f.write(cookies_content)
            logger.info(f"Created cookies file from base64, size: {len(cookies_content)} bytes")
        except Exception as e:
            logger.error(f"Error creating cookies file from base64: {e}")
    # Create cookies file from environment variable if provided
    elif cookies_env:
        try:
            with open(cookies_file, "w") as f:
                f.write(cookies_env)
            logger.info(f"Created cookies file from environment variable, size: {len(cookies_env)} bytes")
        except Exception as e:
            logger.error(f"Error creating cookies file: {e}")
    
    # Check if cookies file exists
    cookies_exist = os.path.exists(cookies_file)
    logger.info(f"Cookies file exists: {cookies_exist}")
    if cookies_exist:
        cookies_size = os.path.getsize(cookies_file)
        logger.info(f"Cookies file size: {cookies_size} bytes")
    
    ydl_opts = {
        "outtmpl": os.path.join(TEMP_DIR, temp_filename + ".%(ext)s"),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "socket_timeout": 60,
        "retries": 10,
        "no_check_certificates": True,
        "legacyserverconnect": True,
        # Add user agent to avoid bot detection
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Add additional options to bypass YouTube restrictions
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
            }
        },
        "extract_flat": False,
        "fragment_retries": 10,
    }
    
    # Use cookies if file exists
    if os.path.exists(cookies_file):
        ydl_opts["cookiefile"] = cookies_file
        logger.info("Using cookies file for authentication")
    else:
        logger.warning("No cookies file found, proceeding without authentication")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_file = ydl.prepare_filename(info)
            # yt-dlp puede cambiar la extensión al hacer merge
            if not os.path.exists(temp_file):
                temp_file = os.path.splitext(temp_file)[0] + ".mp4"
            
            # Get the original video title for the download filename
            video_title = info.get('title', 'video')
            # Clean the title to make it safe for filenames
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).strip()
            download_filename = f"{safe_title}.mp4"
            
            # Register cleanup function to delete the file after sending
            @after_this_request
            def remove_file(response):
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        logger.info(f"Deleted temporary file: {temp_file}")
                except Exception as e:
                    logger.error(f"Error deleting temporary file: {e}")
                return response
            
            # Send the file to the client
            return send_file(
                temp_file,
                as_attachment=True,
                download_name=download_filename,
                mimetype='video/mp4'
            )
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use 0.0.0.0 to make it accessible from outside the container
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", debug=debug, port=port)
