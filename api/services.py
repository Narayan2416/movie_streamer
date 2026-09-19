from flask import Flask, Response, request,Blueprint
from db.moviesDb import getMovieById,getMovies
import os

bp=Blueprint("apis",__name__)

@bp.route("/api/movies/play/<int:id>")
def video(id):
    movie = getMovieById(id)
    VIDEO_PATH = movie.get("movie_path")
    mime_type = movie.get("mime_type")

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
            mimetype="video/"+mime_type,
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
        mimetype="video/"+mime_type,
        headers={
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length
            )
        }
    )

@bp.route("/api/movies", methods=["GET"])
def getMoviesAPI():
    movies = getMovies()
    return {"movies": movies}, 200

@bp.route("/api/movies/<int:id>/type", methods=["GET"])
def getMovieType(id):
    movie = getMovieById(id)
    if movie:
        return {"type": movie.get("mime_type")}, 200
    return {"error": "Movie not found"}, 404