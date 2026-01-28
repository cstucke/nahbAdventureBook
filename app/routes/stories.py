from flask import Blueprint, jsonify

stories_bp = Blueprint("stories", __name__, url_prefix="/stories")


@stories_bp.route("/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Hello"})
