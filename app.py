from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Download route
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "❌ No URL provided!"

    temp_file = "/tmp/song.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": temp_file,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"❌ Download error: {str(e)}"

    if os.path.exists(temp_file):
        return send_file(
            temp_file,
            as_attachment=True,
            download_name="song.mp3",
            mimetype="audio/mpeg"
        )
    else:
        return "❌ MP3 file not found after conversion!"

if __name__ == "__main__":
    app.run(debug=True)