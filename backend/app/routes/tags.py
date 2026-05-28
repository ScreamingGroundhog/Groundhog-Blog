from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Tag
from app import db
from app.routes import tags_bp
import re


@tags_bp.route("", methods=["GET"])
@jwt_required()
def get_tags():
    tags = Tag.query.order_by(Tag.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tags]), 200


@tags_bp.route("", methods=["POST"])
@jwt_required()
def create_tag():
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "标签名不能为空"}), 400

    slug = re.sub(r"[\s_-]+", "-", re.sub(r"[^\w\s-]", "", name.lower().strip()))
    if Tag.query.filter_by(slug=slug).first():
        return jsonify({"error": "该标签名已存在"}), 409

    tag = Tag(name=name, slug=slug)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201


@tags_bp.route("/<int:tag_id>", methods=["PUT"])
@jwt_required()
def update_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "标签不存在"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    if "name" in data:
        tag.name = data["name"]

    db.session.commit()
    return jsonify(tag.to_dict()), 200


@tags_bp.route("/<int:tag_id>", methods=["DELETE"])
@jwt_required()
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"error": "标签不存在"}), 404
    tag.articles = []
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "删除成功"}), 200
