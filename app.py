from flask import Flask, request, jsonify, render_template
import requests
import random
mood_map = {
    "funny": "comedy books",
    "romance": "romantic novels",
    "sad": "emotional novels",
    "horror": "horror books",
    "thriller": "thriller novels",
    "motivation": "self help books",
    "love": "romantic novels",
    "study": "educational books",
    "history": "history books"
}

app = Flask(__name__)

# 🔥 Fetch books from Google API
def fetch_books(query):

    original_query = query
    query = query.lower()

    # mood mapping
    for mood in mood_map:
        if mood in query:
            query = mood_map[mood]
            break
    else:
        query = original_query

    # 🔥 IMPORTANT: simple query rakho (intitle hata diya)
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    res = requests.get(url).json()
    books = []

    if "items" in res:
        for item in res["items"][:10]:
            info = item["volumeInfo"]

            rating = info.get("averageRating")
            reviews = info.get("ratingsCount")

            # fallback values
            if not rating:
                rating = round(random.uniform(3.5, 4.8), 1)

            if not reviews:
                reviews = random.randint(50, 5000)

            books.append({
                "title": info.get("title", "No Title"),
                "author": ", ".join(info.get("authors", ["Unknown"])),
                "thumbnail": info.get("imageLinks", {}).get(
                    "thumbnail",
                    "https://via.placeholder.com/150"
                ),
                "rating": rating,
                "reviews": reviews
            })

    return books


# 🏠 Home page (Top books)
@app.route("/")
def home():
    top_books = fetch_books("bestseller")
    return render_template("index.html", top_books=top_books)


# 🔍 Recommendation route
@app.route("/recommend")
def recommend():
    query = request.args.get("q")
    results = fetch_books(query)
    return jsonify(results)


# 🚀 Run app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)