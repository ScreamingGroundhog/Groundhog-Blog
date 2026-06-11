from flask import request, jsonify
from sqlalchemy.orm import joinedload
from app.models import Article, Category, Tag, User
from app import db
from app.routes import public_bp


@public_bp.route("/articles", methods=["GET"])
def get_articles():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category_id = request.args.get("category_id", type=int)
    tag_id = request.args.get("tag_id", type=int)
    keyword = request.args.get("keyword", "")

    query = Article.query.options(
        joinedload(Article.category), joinedload(Article.tags)
    ).filter(Article.status == "published")

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
        "items": [article.to_public_dict() for article in pagination.items],
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "pages": pagination.pages,
    }), 200


@public_bp.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article = Article.query.options(
        joinedload(Article.category), joinedload(Article.tags)
    ).filter(Article.id == article_id, Article.status == "published").first()

    if not article:
        return jsonify({"error": "文章不存在"}), 404

    article.view_count += 1
    db.session.commit()

    return jsonify(article.to_public_dict()), 200


@public_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return jsonify([c.to_dict() for c in categories]), 200


@public_bp.route("/tags", methods=["GET"])
def get_tags():
    tags = Tag.query.order_by(Tag.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tags]), 200


@public_bp.route("/articles/<int:article_id>/nearby", methods=["GET"])
def get_nearby_articles(article_id):
    article = Article.query.get(article_id)
    if not article or article.status != "published":
        return jsonify({"prev": None, "next": None}), 200

    prev_article = (
        Article.query.filter(
            Article.status == "published",
            Article.id < article.id,
        )
        .order_by(Article.id.desc())
        .first()
    )

    next_article = (
        Article.query.filter(
            Article.status == "published",
            Article.id > article.id,
        )
        .order_by(Article.id.asc())
        .first()
    )

    return jsonify({
        "prev": prev_article.to_public_dict() if prev_article else None,
        "next": next_article.to_public_dict() if next_article else None,
    }), 200


@public_bp.route("/about", methods=["GET"])
def get_about():
    user = User.query.first()
    return jsonify({
        "nickname": user.nickname if user else "Admin",
        "avatar": user.avatar if user else "",
        "description": "一只渴望成为技术大牛的土拨鼠",
        "github": "https://github.com/ScreamingGroundhog",
    }), 200
