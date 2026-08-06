import os
import json
from flask import Flask, render_template, request, jsonify

# وارد کردن کلاس‌های هسته پروژه شما
from core.graph import Graph
from core.BFS import BFS
from core.DFS import DFS
from core.statistics import Statistics
from core.recommendation import Recommendation
from models.user import User
from core.exceptions import DuplicateUser, UserNotFound, DuplicateEdge, InvalidEdge

app = Flask(__name__)

# مقداردهی اولیه گراف
graph = Graph()
DATA_FILE = "social_network_data.json"

# ==========================================
# JSON Persistence (بخش 11 صورت‌مسئله)
# ==========================================
def save_data():
    """ذخیره وضعیت فعلی گراف در فایل JSON"""
    data = {"users": [], "edges": []}
    
    # ذخیره کاربران
    for user in graph.get_users():
        data["users"].append({
            "id": user.id, 
            "name": getattr(user, 'name', str(user.id)),
            "username": getattr(user, 'username', '')
        })
        
    # ذخیره یال‌ها (روابط)
    seen_edges = set()
    for user_id in graph.user_ids():
        for friend_id in graph.get_neighbors(user_id):
            edge = tuple(sorted([str(user_id), str(friend_id)]))
            if edge not in seen_edges:
                data["edges"].append({"source": edge[0], "target": edge[1]})
                seen_edges.add(edge)
                
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    """بازیابی گراف از فایل JSON در صورت وجود"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for u in data.get("users", []):
                    # ساخت آبجکت کاربر. 
                    # اگر کلاس User شما پارامترهای دیگری دارد اینجا تنظیم کنید.
                    user = User(u["id"])
                    user.name = u.get("name", "")
                    user.username = u.get("username", "")
                    graph.add_user(user)
                    
                for e in data.get("edges", []):
                    try:
                        graph.add_edge(e["source"], e["target"])
                    except Exception:
                        pass
            except json.JSONDecodeError:
                pass

# لود کردن دیتا هنگام اجرای برنامه
load_data()

# توابع کمکی برای تبدیل ID
def parse_id(uid):
    """تلاش برای تبدیل آیدی به عدد (در صورت نیاز)"""
    try:
        return int(uid)
    except ValueError:
        return uid

# ==========================================
# Web UI Route
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

# ==========================================
# API Endpoints
# ==========================================

@app.route("/api/graph", methods=["GET"])
def get_graph_data():
    """دریافت دیتای گراف برای رسم در vis.js"""
    nodes = []
    for user in graph.get_users():
        nodes.append({
            "id": user.id,
            "label": getattr(user, 'name', str(user.id)),
            "title": f"ID: {user.id}"
        })
        
    edges = []
    seen = set()
    for user_id in graph.user_ids():
        for friend_id in graph.get_neighbors(user_id):
            edge_id = tuple(sorted([str(user_id), str(friend_id)]))
            if edge_id not in seen:
                edges.append({"from": edge_id[0], "to": edge_id[1]})
                seen.add(edge_id)
                
    return jsonify({"nodes": nodes, "edges": edges})

@app.route("/api/users", methods=["POST", "PUT", "DELETE"])
def manage_users():
    """افزودن، ویرایش و حذف کاربران"""
    if request.method == "POST":
        data = request.json
        uid = parse_id(data.get("id"))
        name = data.get("name")
        
        user = User(uid)
        user.name = name
        
        try:
            graph.add_user(user)
            save_data()
            return jsonify({"status": "success", "message": f"کاربر {name} اضافه شد."})
        except DuplicateUser as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    elif request.method == "PUT":
        data = request.json
        uid = parse_id(data.get("id"))
        new_name = data.get("name")
        try:
            user = graph.get_user(uid)
            user.name = new_name
            save_data()
            return jsonify({"status": "success", "message": "اطلاعات کاربر بروزرسانی شد."})
        except UserNotFound as e:
            return jsonify({"status": "error", "message": str(e)}), 404
            
    elif request.method == "DELETE":
        data = request.json
        uid = parse_id(data.get("id"))
        try:
            graph.remove_user(uid)
            save_data()
            return jsonify({"status": "success", "message": "کاربر حذف شد."})
        except UserNotFound as e:
            return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/edges", methods=["POST", "DELETE"])
def manage_edges():
    """افزودن و حذف دوستی"""
    data = request.json
    u1 = parse_id(data.get("source"))
    u2 = parse_id(data.get("target"))
    
    if request.method == "POST":
        try:
            graph.add_edge(u1, u2)
            save_data()
            return jsonify({"status": "success", "message": "ارتباط دوستی ایجاد شد."})
        except (UserNotFound, InvalidEdge, DuplicateEdge) as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    elif request.method == "DELETE":
        try:
            graph.remove_edge(u1, u2)
            save_data()
            return jsonify({"status": "success", "message": "ارتباط دوستی حذف شد."})
        except UserNotFound as e:
            return jsonify({"status": "error", "message": str(e)}), 404

# --- پردازش‌های خواسته شده ---

@app.route("/api/friends/<uid>", methods=["GET"])
def get_friends(uid):
    """1. لیست کردن دوستان یک کاربر"""
    uid = parse_id(uid)
    try:
        friends_ids = graph.get_neighbors(uid)
        friends = [{"id": fid, "name": getattr(graph.get_user(fid), 'name', str(fid))} for fid in friends_ids]
        return jsonify({"status": "success", "data": friends})
    except UserNotFound as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/connection/<u1>/<u2>", methods=["GET"])
def check_connection(u1, u2):
    """2. آیا دو کاربر با هم مرتبط هستند؟"""
    u1, u2 = parse_id(u1), parse_id(u2)
    try:
        connected = graph.has_edge(u1, u2)
        return jsonify({"status": "success", "connected": connected})
    except UserNotFound as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/path/<u1>/<u2>", methods=["GET"])
def get_shortest_path(u1, u2):
    """3. پیدا کردن کوتاه‌ترین مسیر"""
    u1, u2 = parse_id(u1), parse_id(u2)
    try:
        bfs = BFS(graph)
        path = bfs.shortest_path(u1, u2)
        formatted = bfs.format_path(path)
        return jsonify({"status": "success", "path": formatted})
    except UserNotFound as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/recommend/<uid>", methods=["GET"])
def recommend_friends(uid):
    """4. پیشنهاد دوست"""
    uid = parse_id(uid)
    try:
        rec = Recommendation(graph)
        suggestions = rec.recommend(uid)
        res = [{"id": u.id, "name": getattr(u, 'name', str(u.id)), "score": s} for u, s in suggestions]
        return jsonify({"status": "success", "recommendations": res})
    except UserNotFound as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/groups", methods=["GET"])
def get_groups():
    """5. لیست کردن گروه‌های شبکه"""
    dfs = DFS(graph)
    components = dfs.connected_components()
    formatted = dfs.format_components(components)
    return jsonify({"status": "success", "groups": formatted})

@app.route("/api/mutual/<u1>/<u2>", methods=["GET"])
def get_mutual_friends(u1, u2):
    """7. دوستان مشترک دو کاربر"""
    u1, u2 = parse_id(u1), parse_id(u2)
    try:
        f1 = graph.get_neighbors(u1)
        f2 = graph.get_neighbors(u2)
        mutual_ids = f1.intersection(f2)
        mutual = [{"id": mid, "name": getattr(graph.get_user(mid), 'name', str(mid))} for mid in mutual_ids]
        return jsonify({"status": "success", "mutual": mutual})
    except UserNotFound as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """8. محاسبه اطلاعات شبکه (شامل 6)"""
    stats = Statistics(graph)
    try:
        summary = stats.summary()
        # Format the user objects for JSON serialization
        if summary["most_connected_user"]:
            u_id = summary["most_connected_user"]["id"]
            summary["most_connected_user"]["name"] = getattr(graph.get_user(u_id), 'name', str(u_id))
            
        summary["largest_group_members"] = [
            getattr(graph.get_user(uid), 'name', str(uid)) for uid in summary["largest_group_members"]
        ]
        return jsonify({"status": "success", "stats": summary})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/distances/<uid>", methods=["GET"])
def get_distances(uid):
    """9. فاصله کاربر از تمام افراد"""
    uid = parse_id(uid)
    try:
        bfs = BFS(graph)
        distances = bfs.distance_to_all(uid)
        formatted = bfs.format_distances(distances)
        # مرتب‌سازی از کمترین فاصله به بیشترین
        sorted_dist = dict(sorted(formatted.items(), key=lambda item: item[1]))
        return jsonify({"status": "success", "distances": sorted_dist})
    except UserNotFound as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    """ایمپورت گروهی کاربران و روابط از فایل txt با تخصیص خودکار آیدی عددی"""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "فایلی ارسال نشده است."}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "فایلی انتخاب نشده است."}), 400
        
    try:
        content = file.read().decode('utf-8')
        lines = content.splitlines()
        
        users_added = 0
        edges_added = 0
        
        # پیدا کردن بزرگترین آیدی عددی موجود در گراف برای اینکه از ادامه اون شروع کنیم (مثلا از ۱)
        existing_ids = []
        for uid in graph.user_ids():
            try:
                existing_ids.append(int(uid))
            except ValueError:
                pass
                
        next_id = max(existing_ids + [0]) + 1
        
        # دیکشنری برای نگهداری مپینگ حروف/کلمات به آیدی‌های عددی جدید
        token_to_id = {} 
        
        for line in lines:
            line = line.strip()
            # رد کردن خطوط خالی یا کامنت‌ها
            if not line or line.startswith('#'):
                continue
                
            parts = line.split()
            if len(parts) >= 1:
                token1 = parts[0]
                
                # اگر این کاراکتر/اسم رو قبلا ندیدیم، یک آیدی عددی بهش میدیم
                if token1 not in token_to_id:
                    token_to_id[token1] = next_id
                    user = User(id=next_id)
                    user.name = token1  # اسم کاربر رو همون چیزی میذاریم که تو فایله
                    
                    if not graph.has_user(next_id):
                        graph.add_user(user)
                        users_added += 1
                    next_id += 1
                    
                u1 = token_to_id[token1]
                
                if len(parts) >= 2:
                    token2 = parts[1]
                    
                    if token2 not in token_to_id:
                        token_to_id[token2] = next_id
                        user = User(id=next_id)
                        user.name = token2
                        
                        if not graph.has_user(next_id):
                            graph.add_user(user)
                            users_added += 1
                        next_id += 1
                        
                    u2 = token_to_id[token2]
                    
                    try:
                        # جلوگیری از ایجاد دوستی کاربر با خودش
                        if u1 != u2:
                            graph.add_edge(u1, u2)
                            edges_added += 1
                    except (DuplicateEdge, InvalidEdge):
                        pass
                        
        save_data()
        return jsonify({
            "status": "success", 
            "message": f"دیتاست با موفقیت اعمال شد. {users_added} کاربر با آیدی عددی یکتا و {edges_added} رابطه جدید ساخته شد."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در پردازش فایل: {str(e)}"}), 500

if __name__ == "__main__":
    # اجرای سرور روی پورت 5000
    app.run(debug=True, port=5000)