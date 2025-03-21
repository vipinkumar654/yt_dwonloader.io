from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

# Temporary folder to store downloaded videos
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        
        if not url:
            return "Please enter a valid YouTube URL", 400
        
        try:
            # Download video
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            return send_file(filename, as_attachment=True)

        except Exception as e:
            return f"Error: {str(e)}", 500

    return '''
    <h2>YouTube Video Downloader</h2>
    <form method="post">
        <input type="text" name="url" placeholder="Enter YouTube URL" required>
        <button type="submit">Download</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)