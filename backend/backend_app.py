from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(BASE_DIR, "posts.json")

def load_posts():
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("📄 Loaded posts:", data)
                return data
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON Decode Error: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Error loading file: {e}")
            return []
    else:
        print("⚠️ posts.json not found")
        return []

def save_posts(posts):
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = load_posts()
    sort_by = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    valid_sort_fields = {'title', 'content'}
    valid_directions = {'asc', 'desc'}

    if sort_by and sort_by not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field '{sort_by}'. Must be 'title' or 'content'."}), 400

    if direction and direction not in valid_directions:
        return jsonify({"error": f"Invalid sort direction '{direction}'. Must be 'asc' or 'desc'."}), 400

    if sort_by:
        reverse = direction == 'desc'
        posts.sort(key=lambda post: post[sort_by].lower(), reverse=reverse)

    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def add_post():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON data."}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({"error": "Both 'title' and 'content' are required and cannot be empty."}), 400

    posts = load_posts()
    new_id = max((post['id'] for post in posts), default=0) + 1
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    posts.append(new_post)
    save_posts(posts)

    return jsonify(new_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == id), None)

    if post is None:
        return jsonify({"error": "Post not found."}), 404

    posts.remove(post)
    save_posts(posts)

    return jsonify({"message": f"Post with ID {id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    posts = load_posts()
    post = next((post for post in posts if post["id"] == id), None)

    if post is None:
        return jsonify({"error": f"Post with ID {id} not found."}), 404

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON data."}), 400

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
        return jsonify({"error": "Both 'title' and 'content' are required and cannot be empty."}), 400

    post["title"] = title
    post["content"] = content
    save_posts(posts)

    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    posts = load_posts()
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    def matches(post):
        in_title = title_query in post['title'].lower() if title_query else False
        in_content = content_query in post['content'].lower() if content_query else False
        return in_title or in_content

    filtered_posts = [post for post in posts if matches(post)]
    return jsonify(filtered_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
