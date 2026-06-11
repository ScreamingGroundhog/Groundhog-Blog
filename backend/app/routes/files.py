import os
import re
import uuid
from flask import request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.routes import files_bp


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def safe_filename(name):
    """Sanitize a filename: strip path separators and dangerous chars, but keep Unicode."""
    name = name.replace("\\", "/")
    name = os.path.basename(name)
    name = re.sub(r"[\x00-\x1f]", "", name)
    name = name.strip(". ")
    return name


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

    ext = file.filename.rsplit(".", 1)[1].lower()

    custom_name = request.form.get("name", "").strip()
    if custom_name:
        custom_name = safe_filename(custom_name)
        if not custom_name:
            custom_name = uuid.uuid4().hex
        if "." not in custom_name:
            custom_name = f"{custom_name}.{ext}"
        final_name = custom_name
    else:
        final_name = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, final_name)
    file.save(filepath)

    url = f"/api/files/{final_name}"
    return jsonify({"url": url, "filename": final_name}), 201


@files_bp.route("/<filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@files_bp.route("/<filename>", methods=["DELETE"])
@jwt_required()
def delete_file(filename):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user and user.avatar:
        avatar_name = user.avatar.rsplit("/", 1)[-1]
        if filename == avatar_name:
            return jsonify({"error": "当前头像文件不允许手动删除，更换头像时将自动移除旧文件"}), 403

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)

    if not os.path.isfile(filepath):
        return jsonify({"error": "文件不存在"}), 404

    os.remove(filepath)
    return jsonify({"message": "删除成功"}), 200
