from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
from app.models import Article, Category, Tag, article_tags
from app import db
from app.routes import articles_bp
from datetime import datetime
import re


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def unique_slug(base_slug, current_id=None):
    slug = base_slug
    counter = 1
    while True:
        query = Article.query.filter_by(slug=slug)
        if current_id:
            query = query.filter(Article.id != current_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


@articles_bp.route("", methods=["GET"])
@jwt_required()
def get_articles():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status", "")
    category_id = request.args.get("category_id", type=int)
    tag_id = request.args.get("tag_id", type=int)
    keyword = request.args.get("keyword", "")

    query = Article.query.options(joinedload(Article.category), joinedload(Article.tags))

    if status:
        query = query.filter(Article.status == status)
    if category_id:
        query = query.filter(Article.category_id == category_id)
    if tag_id:
        query = query.filter(Article.tags.any(Tag.id == tag_id))
    if keyword:
        query = query.filter(
            (Article.title.contains(keyword)) | (Article.content.contains(keyword))
        )

    query = query.order_by(Article.is_pinned.desc(), Article.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": [article.to_dict() for article in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
    }), 200


@articles_bp.route("/<int:article_id>", methods=["GET"])
@jwt_required()
def get_article(article_id):
    article = Article.query.options(
        joinedload(Article.category), joinedload(Article.tags)
    ).get(article_id)
    if not article:
        return jsonify({"error": "文章不存在"}), 404
    return jsonify(article.to_dict()), 200


@articles_bp.route("", methods=["POST"])
@jwt_required()
def create_article():
    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "标题不能为空"}), 400

    article = Article(
        title=title,
        slug=unique_slug(slugify(title)),
        summary=data.get("summary", ""),
        content=data.get("content", ""),
        cover_image=data.get("cover_image", ""),
        status=data.get("status", "draft"),
        is_pinned=data.get("is_pinned", False),
        category_id=data.get("category_id"),
    )

    tag_ids = data.get("tag_ids", [])
    if tag_ids:
        article.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(article)
    db.session.commit()

    article = Article.query.options(
        joinedload(Article.category), joinedload(Article.tags)
    ).get(article.id)
    return jsonify(article.to_dict()), 201


@articles_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    article = Article.query.options(
        joinedload(Article.category), joinedload(Article.tags)
    ).get(article_id)
    if not article:
        return jsonify({"error": "文章不存在"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    if "title" in data:
        article.title = data["title"]
        article.slug = unique_slug(slugify(data["title"]), article.id)
    if "summary" in data:
        article.summary = data["summary"]
    if "content" in data:
        article.content = data["content"]
    if "cover_image" in data:
        article.cover_image = data["cover_image"]
    if "status" in data:
        article.status = data["status"]
    if "is_pinned" in data:
        article.is_pinned = data["is_pinned"]
    if "category_id" in data:
        article.category_id = data["category_id"]
    if "tag_ids" in data:
        article.tags = Tag.query.filter(Tag.id.in_(data["tag_ids"])).all()

    db.session.commit()
    return jsonify(article.to_dict()), 200


@articles_bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": "文章不存在"}), 404
    db.session.delete(article)
    db.session.commit()
    return jsonify({"message": "删除成功"}), 200
