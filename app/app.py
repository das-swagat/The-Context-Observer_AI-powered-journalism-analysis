from flask import Flask, render_template, request, jsonify
from analyzer_core import analyze_article
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"ok": True, "status": "running"})


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        payload = request.get_json(force=True) or {}

        article_text = payload.get("article_text", "") or ""
        article_url = payload.get("article_url", "") or ""

        result = analyze_article(
            article_text=article_text,
            article_url=article_url
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": f"Server error during analysis: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
