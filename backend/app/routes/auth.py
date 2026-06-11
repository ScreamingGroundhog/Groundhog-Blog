import os

from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from app.routes import auth_bp


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "用户名或密码错误"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "description": user.description,
            "blog_description": user.blog_description,
        }
    }), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")
    nickname = data.get("nickname", username)

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    if len(password) < 6:
        return jsonify({"error": "密码长度不能少于6位"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 409

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        nickname=nickname,
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "description": user.description,
            "blog_description": user.blog_description,
        }
    }), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "description": user.description,
        "blog_description": user.blog_description,
    }), 200


@auth_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    if "nickname" in data:
        user.nickname = data["nickname"]
    if "avatar" in data:
        old = user.avatar or ""
        new = data["avatar"] or ""
        if old != new and old.startswith("/api/files/"):
            old_name = old.rsplit("/", 1)[-1]
            old_path = os.path.join(current_app.config["UPLOAD_FOLDER"], old_name)
            if os.path.isfile(old_path):
                os.remove(old_path)
        user.avatar = data["avatar"]
    if "description" in data:
        user.description = data["description"]
    if "blog_description" in data:
        user.blog_description = data["blog_description"]
    if "new_password" in data and data["new_password"]:
        old_password = data.get("old_password", "")
        if not old_password or not check_password_hash(user.password_hash, old_password):
            return jsonify({"error": "原密码错误"}), 403
        if len(data["new_password"]) < 6:
            return jsonify({"error": "新密码长度不能少于6位"}), 400
        user.password_hash = generate_password_hash(data["new_password"])

    db.session.commit()
    return jsonify({
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "description": user.description,
        "blog_description": user.blog_description,
    }), 200
