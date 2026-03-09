from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, date
import json, os, uuid

app = Flask(__name__)

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2, default=str)

# ─── ROUTES ───────────────────────────────────────────────

@app.route("/")
def index():
    tasks = load_tasks()
    stats = compute_stats(tasks)
    return render_template("index.html", tasks=tasks, stats=stats)

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    # Filtres
    status   = request.args.get("status")        # all | active | completed
    priority = request.args.get("priority")      # low | medium | high
    category = request.args.get("category")
    search   = request.args.get("search", "").lower()

    if status == "active":
        tasks = [t for t in tasks if not t["completed"]]
    elif status == "completed":
        tasks = [t for t in tasks if t["completed"]]

    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]
    if category:
        tasks = [t for t in tasks if t.get("category") == category]
    if search:
        tasks = [t for t in tasks if search in t["title"].lower()
                 or search in t.get("description", "").lower()]

    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data  = request.get_json()
    tasks = load_tasks()

    task = {
        "id":          str(uuid.uuid4()),
        "title":       data.get("title", "").strip(),
        "description": data.get("description", "").strip(),
        "priority":    data.get("priority", "medium"),
        "category":    data.get("category", "General"),
        "due_date":    data.get("due_date", ""),
        "tags":        data.get("tags", []),
        "completed":   False,
        "created_at":  datetime.now().isoformat(),
        "updated_at":  datetime.now().isoformat(),
        "subtasks":    [],
    }

    if not task["title"]:
        return jsonify({"error": "Title required"}), 400

    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data  = request.get_json()
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            for key in ["title", "description", "priority", "category",
                        "due_date", "tags", "completed", "subtasks"]:
                if key in data:
                    task[key] = data[key]
            task["updated_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            return jsonify(task)

    return jsonify({"error": "Not found"}), 404

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"ok": True})

@app.route("/api/tasks/bulk", methods=["POST"])
def bulk_action():
    data   = request.get_json()
    action = data.get("action")   # delete | complete | uncomplete
    ids    = set(data.get("ids", []))
    tasks  = load_tasks()

    for task in tasks:
        if task["id"] in ids:
            if action == "complete":
                task["completed"] = True
            elif action == "uncomplete":
                task["completed"] = False

    if action == "delete":
        tasks = [t for t in tasks if t["id"] not in ids]

    save_tasks(tasks)
    return jsonify({"ok": True, "affected": len(ids)})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    tasks = load_tasks()
    return jsonify(compute_stats(tasks))

# ─── HELPERS ──────────────────────────────────────────────

def compute_stats(tasks):
    total     = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    overdue   = 0
    today_str = date.today().isoformat()

    for t in tasks:
        if not t["completed"] and t.get("due_date") and t["due_date"] < today_str:
            overdue += 1

    by_priority = {"high": 0, "medium": 0, "low": 0}
    for t in tasks:
        p = t.get("priority", "medium")
        by_priority[p] = by_priority.get(p, 0) + 1

    by_category = {}
    for t in tasks:
        c = t.get("category", "General")
        by_category[c] = by_category.get(c, 0) + 1

    return {
        "total":       total,
        "completed":   completed,
        "active":      total - completed,
        "overdue":     overdue,
        "completion":  round((completed / total * 100) if total else 0, 1),
        "by_priority": by_priority,
        "by_category": by_category,
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)
