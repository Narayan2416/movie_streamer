from flask import Flask, Response, request,Blueprint
from db.moviesDb import getMovieById
import os

bp=Blueprint("apis",__name__)

@bp.route("/video/<int:id>")
def video(id):
    VIDEO_PATH = getMovieById(id).get("movie_path")
    #print(VIDEO_PATH,"has path?")

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