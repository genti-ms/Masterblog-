from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Flask tutorial", "content": "Learn how to use Flask in this post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)

    if page < 1 or limit < 1:
        return jsonify({"error": "Page and limit must be greater than 0."}), 400

    # Paginierung und Sortierung der Posts
    sorted_posts = POSTS
    if sort_field:
        if sort_field not in ('title', 'content'):
            return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400
        if direction not in ('asc', 'desc'):
            return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

        reverse = direction == 'desc'
        sorted_posts = sorted(POSTS, key=lambda post: post[sort_field].lower(), reverse=reverse)

    start = (page - 1) * limit
    end = start + limit
    paginated_posts = sorted_posts[start:end]

    total_posts = len(POSTS)
    total_pages = (total_posts + limit - 1) // limit

    return jsonify({
        'total_posts': total_posts,
        'page': page,
        'limit': limit,
        'total_pages': total_pages,
        'posts': paginated_posts
    })

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
    post = next((post for post in POSTS if post["id"] == id), None)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    data = request.get_json()

    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])

    return jsonify({
        "id": post["id"],
        "title": post["title"],
        "content": post["content"]
    }), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    def matches(post):
        matches_title = title_query in post['title'].lower() if title_query else False
        matches_content = content_query in post['content'].lower() if content_query else False
        return matches_title or matches_content

    filtered_posts = [post for post in POSTS if matches(post)]

    return jsonify(filtered_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
