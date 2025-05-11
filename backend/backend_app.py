from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Both 'title' and 'content' are required."}), 400

    new_id = max(post['id'] for post in POSTS) + 1
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = next((post for post in POSTS if post['id'] == id), None)

    if post is None:
        return jsonify({"error": "Post not found."}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Suche den Post mit der angegebenen ID
    post = next((post for post in POSTS if post["id"] == id), None)

    # Falls der Post nicht existiert, gib eine 404 Fehlerantwort zurück
    if post is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    # Hol die neuen Daten aus der Anfrage
    data = request.get_json()

    # Aktualisiere den Titel und Inhalt, falls diese im Body angegeben sind
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    # Rückgabe des aktualisierten Posts
    return jsonify({
        "id": post["id"],
        "title": post["title"],
        "content": post["content"]
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
