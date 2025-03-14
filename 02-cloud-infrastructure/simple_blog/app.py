from flask import Flask, render_template, request
import json
from datetime import datetime, timezone

app = Flask(__name__)

# Load existing posts (empty list initially)
posts = []

@app.route("/", methods=["GET", "POST"])
def index():
  # Load existing posts (before any POST request)
  with open("posts.json", "r") as f:
      posts = json.load(f)  
  if request.method == "POST":
    # Get form data
    name = request.form.get("name")
    title = request.form.get("title")
    content = request.form.get("content")

    # Create a new post
    post = {
      "name": name,
      "title": title,
      "content": content,
      "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # Add post to list and save to JSON
    posts.append(post)
    with open("posts.json", "w") as f:
      json.dump(posts, f, indent=4)

  # Load posts from JSON
  with open("posts.json", "r") as f:
    posts = json.load(f)

  # Convert timestamps to human-friendly format
  for post in posts:
    post["timestamp"] = datetime.fromisoformat(post["timestamp"]).strftime("%B %d, %Y at %I:%M %p")

  return render_template("index.html", posts=posts)

if __name__ == "__main__":  
  app.run(debug=True)