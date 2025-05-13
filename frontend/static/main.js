let editingPostId = null;

async function loadPosts() {
    const apiBaseUrl = document.getElementById("api-base-url").value;
    const response = await fetch(`${apiBaseUrl}/posts`);

    if (!response.ok) {
        alert("Failed to load posts.");
        return;
    }

    const posts = await response.json();
    const container = document.getElementById("post-container");
    container.innerHTML = "";

    posts.forEach(post => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";

        const title = document.createElement("h2");
        title.textContent = post.title;

        const content = document.createElement("p");
        content.textContent = post.content;

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.onclick = () => editPost(post.id);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deletePost(post.id);

        postDiv.appendChild(title);
        postDiv.appendChild(content);
        postDiv.appendChild(editButton);
        postDiv.appendChild(deleteButton);

        container.appendChild(postDiv);
    });
}

async function addPost() {
    const apiBaseUrl = document.getElementById("api-base-url").value;
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;

    if (!title || !content) {
        alert("Title and content are required.");
        return;
    }

    const response = await fetch(`${apiBaseUrl}/posts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, content })
    });

    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.error}`);
        return;
    }

    document.getElementById("post-title").value = "";
    document.getElementById("post-content").value = "";

    loadPosts();
}

async function deletePost(id) {
    const apiBaseUrl = document.getElementById("api-base-url").value;
    const response = await fetch(`${apiBaseUrl}/posts/${id}`, {
        method: 'DELETE'
    });

    if (!response.ok) {
        alert("Failed to delete post.");
        return;
    }

    loadPosts();
}

async function editPost(postId) {
    const apiBaseUrl = document.getElementById("api-base-url").value;
    const response = await fetch(`${apiBaseUrl}/posts/${postId}`);
    const post = await response.json();

    document.getElementById("edit-title").value = post.title;
    document.getElementById("edit-content").value = post.content;
    document.getElementById("edit-container").style.display = "block";

    editingPostId = postId;
}

async function updatePost() {
    const apiBaseUrl = document.getElementById("api-base-url").value;
    const title = document.getElementById("edit-title").value;
    const content = document.getElementById("edit-content").value;

    if (!title || !content) {
        alert("Title and content are required.");
        return;
    }

    const response = await fetch(`${apiBaseUrl}/posts/${editingPostId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, content })
    });

    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.error}`);
        return;
    }

    document.getElementById("edit-container").style.display = "none";
    loadPosts();
}

function cancelEdit() {
    document.getElementById("edit-container").style.display = "none";
    editingPostId = null;
}
