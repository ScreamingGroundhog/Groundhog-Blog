import os
import uuid
from flask import request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app.routes import files_bp


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@files_bp.route("/list", methods=["GET"])
@jwt_required()
def list_files():
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    files = sorted(
        [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))],
        reverse=True,
    )
    return jsonify(files), 200


@files_bp.route("", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "未选择文件"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "未选择文件"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "不支持的文件类型"}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, unique_name)
    file.save(filepath)

    url = f"/api/files/{unique_name}"
    return jsonify({"url": url, "filename": unique_name}), 201


@files_bp.route("/<filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
