from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Category
from app import db
from app.routes import categories_bp
import re


@categories_bp.route("", methods=["GET"])
@jwt_required()
def get_categories():
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return jsonify([c.to_dict() for c in categories]), 200


@categories_bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "分类名不能为空"}), 400

    slug = re.sub(r"[\s_-]+", "-", re.sub(r"[^\w\s-]", "", name.lower().strip()))
    if Category.query.filter_by(slug=slug).first():
        return jsonify({"error": "该分类名已存在"}), 409

    category = Category(
        name=name,
        slug=slug,
        description=data.get("description", ""),
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@categories_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "分类不存在"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    if "name" in data:
        category.name = data["name"]
    if "description" in data:
        category.description = data["description"]

    db.session.commit()
    return jsonify(category.to_dict()), 200


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "分类不存在"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "删除成功"}), 200
