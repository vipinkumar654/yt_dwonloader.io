from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'cookiefile': 'cookies.txt',  # 👈 If using cookies
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title')
            thumbnail = info.get('thumbnail')

        return jsonify({
            "title": title,
            "thumbnail": thumbnail,
            "download_url": video_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
