from pathlib import Path
import logging
from yt_dlp import YoutubeDL as yt

OUTPUT_DIR = Path.home() / "Music"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUTPUT_DIR / "music.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

def download_audio(url: str) -> None:

    if not url.startswith(("https://", "http://")):
        raise ValueError("A valid HTTP or HTTPS URL is required.")

    options = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
       "outtmpl": str(
            OUTPUT_DIR / "%(uploader)s" / "%(title)s.%(ext)s"
        ),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192K",
            },
            {
                "key": "FFmpegMetadata",
                "add_metadata": True,
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
        "writethumbnail": True,
        "convert_thumbnails": "jpg",
        "writeinfojson": True,
        "ignoreerrors": False,
        "noplaylist": True,
        "overwrites": False,
        "logger": logger,
    }

    try:
        logger.info("Starting authorized audio processing.")
        with yt(options) as ydl:
            ydl.download([url])
        logger.info("Audio processing completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred during audio processing: {e}")
        raise

if __name__ == "__main__":
    url = input(
        "Enter an authorized audio source URL: "
    ).strip()

    if not url:
        raise SystemExit("A source URL is required.")

    download_audio(url)