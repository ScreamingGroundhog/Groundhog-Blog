from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
articles_bp = Blueprint("articles", __name__)
categories_bp = Blueprint("categories", __name__)
tags_bp = Blueprint("tags", __name__)
files_bp = Blueprint("files", __name__)
public_bp = Blueprint("public", __name__)
