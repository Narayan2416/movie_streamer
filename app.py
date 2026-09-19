from flask import Flask, Response, render_template, request,Blueprint
from apis.services import bp as service_bp
import os

app = Flask(__name__)

VIDEO_PATH = "/media/narayanamoorthy/Windows/Users/phnar/Documents/Mollywood Times 2026 Tamil - 1080p HQ HDRip - x264 - DDP 5..mkv"

app.register_blueprint(service_bp, url_prefix="/api")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video")
def video():
    if not os.path.exists(VIDEO_PATH):
        return "Video not found", 404

    file_size = os.path.getsize(VIDEO_PATH)

    range_header = request.headers.get("Range")

    if not range_header:
        def generate():
            with open(VIDEO_PATH, "rb") as f:
                while chunk := f.read(1024 * 1024):
                    yield chunk

        return Response(
            generate(),
            status=200,
            mimetype="video/x-matroska",
            headers={
                "Content-Length": str(file_size),
                "Accept-Ranges": "bytes"
            }
        )

    # Parse Range header
    range_value = range_header.replace("bytes=", "")
    start, end = range_value.split("-")

    start = int(start)

    if end:
        end = int(end)
    else:
        end = file_size - 1

    end = min(end, file_size - 1)

    content_length = end - start + 1

    def generate():
        with open(VIDEO_PATH, "rb") as f:
            f.seek(start)

            remaining = content_length

            while remaining > 0:
                chunk_size = min(1024 * 1024, remaining)
                data = f.read(chunk_size)

                if not data:
                    break

                remaining -= len(data)
                yield data

    return Response(
        generate(),
        status=206,
        mimetype="video/x-matroska",
        headers={
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length
            )
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)