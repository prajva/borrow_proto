from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

# In-memory database for the prototype
items = [
    {
        "id": 1,
        "title": "Casio FX-991ES Scientific Calculator",
        "category": "Electronics",
        "condition": "Excellent",
        "price": "₹10/day",
        "type": "Paid",
        "distance": "200 m",
        "owner": "Rahul M.",
        "image": "https://images.unsplash.com/photo-1594980598776-945f1b1386d3?auto=format&fit=crop&q=80&w=500",
    },
    {
        "id": 2,
        "title": "DBMS Textbook (Korth 7th Edition)",
        "category": "Books",
        "condition": "Good",
        "price": "Free",
        "type": "Free",
        "distance": "450 m",
        "owner": "Ananya S.",
        "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&q=80&w=500",
    },
    {
        "id": 3,
        "title": "Camera Tripod Stand",
        "category": "Photography",
        "condition": "Like New",
        "price": "Exchange",
        "type": "Exchange",
        "distance": "800 m",
        "owner": "Vikram K.",
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&q=80&w=500",
    },
    {
        "id": 4,
        "title": "Compact Rain Umbrella",
        "category": "Daily Utility",
        "condition": "Good",
        "price": "Free",
        "type": "Free",
        "distance": "120 m",
        "owner": "Priya D.",
        "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=500",
    },
]

# Aesthetic HTML Layout using Tailwind CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusShare — Borrow Instead of Buy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

    <!-- Navbar -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <a href="{{ url_for('index') }}" class="flex items-center space-x-2">
                <span class="bg-indigo-600 text-white p-2 rounded-xl font-bold text-lg">📦</span>
                <span class="font-bold text-xl tracking-tight text-slate-900">CampusShare</span>
            </a>
            <div class="flex items-center space-x-4">
                <a href="{{ url_for('index') }}" class="text-sm font-medium text-slate-600 hover:text-indigo-600">Browse</a>
                <a href="{{ url_for('add_item') }}" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-xl shadow-sm transition">
                    + List an Item
                </a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-6 mt-12 text-center text-sm text-slate-500">
        CampusShare Prototype &mdash; Built for College Students (Access over Ownership)
    </footer>

</body>
</html>
"""

INDEX_TEMPLATE = (
    HTML_TEMPLATE
    + """
{% block content %}
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-indigo-900 to-violet-800 rounded-3xl p-8 sm:p-12 mb-10 text-white shadow-xl relative overflow-hidden">
        <div class="relative z-10 max-w-2xl">
            <span class="bg-indigo-500/30 text-indigo-200 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider">Smart Campus Economy</span>
            <h1 class="text-3xl sm:text-4xl font-extrabold mt-4 tracking-tight">Borrow instead of buying for temporary needs.</h1>
            <p class="mt-3 text-indigo-100 text-base sm:text-lg">Save money, reduce clutter, and share resources with students right around your block.</p>
            
            <!-- Search Form -->
            <form action="{{ url_for('index') }}" method="GET" class="mt-6 flex items-center bg-white rounded-2xl p-2 shadow-lg max-w-xl">
                <input type="text" name="q" value="{{ query }}" placeholder="Search calculator, book, tripod..." class="w-full px-4 text-slate-800 focus:outline-none text-sm">
                <button type="submit" class="bg-indigo-600 text-white px-6 py-2.5 rounded-xl font-medium text-sm hover:bg-indigo-700 transition">Search</button>
            </form>
        </div>
    </div>

    <!-- Listings Header -->
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold text-slate-900">Available Near You</h2>
        <span class="text-sm text-slate-500 font-medium">{{ items|length }} items listed</span>
    </div>

    <!-- Items Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {% for item in items %}
        <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-md transition flex flex-col">
            <div class="h-48 w-full bg-slate-100 relative">
                <img src="{{ item.image }}" alt="{{ item.title }}" class="w-full h-full object-cover">
                <span class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-xs font-semibold px-2.5 py-1 rounded-lg text-slate-700 shadow-sm">
                    📍 {{ item.distance }}
                </span>
                <span class="absolute top-3 left-3 bg-indigo-600 text-white text-xs font-semibold px-2.5 py-1 rounded-lg shadow-sm">
                    {{ item.type }}
                </span>
            </div>
            <div class="p-5 flex flex-col flex-grow">
                <div class="text-xs text-indigo-600 font-semibold mb-1 uppercase tracking-wider">{{ item.category }}</div>
                <h3 class="font-bold text-slate-900 text-base mb-2 line-clamp-1">{{ item.title }}</h3>
                <div class="flex items-center justify-between text-sm text-slate-500 mb-4">
                    <span>Condition: <strong class="text-slate-700">{{ item.condition }}</strong></span>
                    <span>By {{ item.owner }}</span>
                </div>
                <div class="mt-auto flex items-center justify-between pt-3 border-t border-slate-100">
                    <span class="font-bold text-slate-900 text-lg">{{ item.price }}</span>
                    <a href="{{ url_for('request_borrow', item_id=item.id) }}" class="bg-indigo-50 text-indigo-600 hover:bg-indigo-600 hover:text-white font-medium text-sm px-4 py-2 rounded-xl transition">
                        Request
                    </a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
{% endblock %}
"""
)

ADD_TEMPLATE = (
    HTML_TEMPLATE
    + """
{% block content %}
<div class="max-w-xl mx-auto bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
    <h2 class="text-2xl font-bold text-slate-900 mb-6">List an Item to Lend</h2>
    <form method="POST" class="space-y-5">
        <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5">Item Title</label>
            <input type="text" name="title" required placeholder="e.g., Casio Scientific Calculator" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm">
        </div>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1.5">Category</label>
                <select name="category" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm bg-white">
                    <option>Electronics</option>
                    <option>Books</option>
                    <option>Photography</option>
                    <option>Daily Utility</option>
                    <option>Sports</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1.5">Condition</label>
                <select name="condition" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm bg-white">
                    <option>Brand New</option>
                    <option>Like New</option>
                    <option>Good</option>
                    <option>Fair</option>
                </select>
            </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1.5">Pricing Type</label>
                <select name="type" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm bg-white">
                    <option>Free</option>
                    <option>Paid</option>
                    <option>Exchange</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1.5">Price / Fee</label>
                <input type="text" name="price" required placeholder="e.g., Free or ₹15/day" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm">
            </div>
        </div>
        <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5">Campus Location / Block</label>
            <input type="text" name="distance" required placeholder="e.g., Block A, 150m away" class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm">
        </div>
        <div>
            <label class="block text-sm font-semibold text-slate-700 mb-1.5">Image URL (Optional)</label>
            <input type="text" name="image" placeholder="https://images.unsplash.com/..." class="w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm">
        </div>
        <div class="pt-4 flex space-x-4">
            <button type="submit" class="flex-1 bg-indigo-600 text-white font-medium py-3 rounded-xl hover:bg-indigo-700 transition shadow-sm">Publish Item</button>
            <a href="{{ url_for('index') }}" class="px-6 py-3 border border-slate-300 font-medium rounded-xl text-slate-700 hover:bg-slate-50 transition text-center">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
"""
)

SUCCESS_TEMPLATE = (
    HTML_TEMPLATE
    + """
{% block content %}
<div class="max-w-md mx-auto bg-white rounded-3xl border border-slate-200 p-8 text-center shadow-sm my-12">
    <div class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto text-2xl mb-4 font-bold">✓</div>
    <h2 class="text-2xl font-bold text-slate-900 mb-2">Request Sent Successfully!</h2>
    <p class="text-slate-600 text-sm mb-6">The item owner has been notified. You can coordinate the campus pickup once they accept.</p>
    <a href="{{ url_for('index') }}" class="inline-block bg-indigo-600 text-white font-medium px-6 py-3 rounded-xl hover:bg-indigo-700 transition">Back to Browse</a>
</div>
{% endblock %}
"""
)


@app.route("/")
def index():
  query = request.args.get("q", "").lower()
  if query:
    filtered_items = [
        item
        for item in items
        if query in item["title"].lower() or query in item["category"].lower()
    ]
  else:
    filtered_items = items
  return render_template_string(
      INDEX_TEMPLATE, items=filtered_items, query=query
  )


@app.route("/add", methods=["GET", "POST"])
def add_item():
  if request.method == "POST":
    new_item = {
        "id": len(items) + 1,
        "title": request.form.get("title"),
        "category": request.form.get("category"),
        "condition": request.form.get("condition"),
        "price": request.form.get("price"),
        "type": request.form.get("type"),
        "distance": request.form.get("distance"),
        "owner": "You (Current User)",
        "image": request.form.get("image")
        or "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&q=80&w=500",
    }
    items.insert(0, new_item)
    return redirect(url_for("index"))
  return render_template_string(ADD_TEMPLATE)


@app.route("/request/<int:item_id>")
def request_borrow(item_id):
  return render_template_string(SUCCESS_TEMPLATE)


if __name__ == "__main__":
  app.run(debug=True)
