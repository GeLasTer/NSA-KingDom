import os
import json
from flask import Flask, request, jsonify, render_template

from core.graph import Graph
from core.BFS import BFS
from core.DFS import DFS
from core.statistics import Statistics
from core.recommendation import Recommendation
from models.user import User
from core.exceptions import DuplicateUser, UserNotFound, DuplicateEdge, InvalidEdge

app = Flask(__name__)
DATA_FILE = 'social_network_data.json'

# ساخت نمونه سراسری گراف
graph = Graph()

def save_data():
    """ذخیره تمام کاربران و روابط در فایل JSON"""
    try:
        data = {"nodes": [], "edges": []}
        
        # ذخیره کاربران
        for u in graph.users():
            data["nodes"].append({"id": u.id, "name": getattr(u, 'name', str(u.id))})
        
        # ذخیره روابط (جلوگیری از ذخیره روابط دوطرفه تکراری)
        visited_edges = set()
        for u in graph.users():
            for v in graph.get_neighbors(u.id):
                # مرتب سازی آیدی ها تا (1,2) با (2,1) یکی در نظر گرفته شود
                pair = tuple(sorted([str(u.id), str(v)]))
                if pair not in visited_edges:
                    visited_edges.add(pair)
                    data["edges"].append({"source": u.id, "target": v})
                    
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    """بازیابی کاربران و روابط از فایل JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # لود کردن کاربران
                for node in data.get("nodes", []):
                    # پاس دادن id به کلاس User برای رفع خطای __init__
                    u = User(id=node["id"])
                    u.name = node.get("name", str(node["id"]))
                    try:
                        graph.add_user(u)
                    except DuplicateUser:
                        pass
                
                # لود کردن یال ها
                for edge in data.get("edges", []):
                    try:
                        graph.add_edge(edge["source"], edge["target"])
                    except (UserNotFound, DuplicateEdge, InvalidEdge):
                        pass
        except Exception as e:
            print(f"Error loading data: {e}")

def parse_id(uid):
    """تبدیل آیدی به عدد در صورت امکان (برای سازگاری با نوع داده‌ها)"""
    if isinstance(uid, str) and uid.isdigit():
        return int(uid)
    return uid

@app.route("/")
def index():
    """سرو کردن فایل HTML فرانت‌اند"""
    return render_template("index.html")

@app.route("/api/graph", methods=["GET"])
def get_graph():
    """ارسال اطلاعات گراف با فرمت قابل فهم برای Vis.js"""
    nodes = [{"id": u.id, "label": getattr(u, 'name', str(u.id))} for u in graph.users()]
    edges = []
    visited_edges = set()
    
    for u in graph.users():
        for v in graph.get_neighbors(u.id):
            pair = tuple(sorted([str(u.id), str(v)]))
            if pair not in visited_edges:
                visited_edges.add(pair)
                edges.append({"from": u.id, "to": v})
                
    return jsonify({"status": "success", "nodes": nodes, "edges": edges})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """دریافت آمار کلی شبکه (تعداد کاربران، روابط، و غیره)"""
    try:
        stat = Statistics(graph)
        summary = stat.summary()
        
        # تبدیل آیدی‌های اعضای بزرگترین گروه به نام نمایشی
        group_names = [getattr(graph.get_user(uid), 'name', str(uid)) for uid in summary.get('largest_group_members', [])]
        summary['largest_group_members'] = group_names
        
        # پیدا کردن تمام کاربرانی که بیشترین ارتباط را دارند (پشتیبانی از تساوی)
        max_degree = -1
        most_connected = []
        
        for uid in graph.user_ids():
            degree = len(graph.get_neighbors(uid))
            if degree > max_degree:
                max_degree = degree
                most_connected = [uid]
            elif degree == max_degree and degree > 0:
                most_connected.append(uid)
                
        if max_degree > 0:
            summary['most_connected_users'] = [
                {"id": uid, "name": getattr(graph.get_user(uid), 'name', str(uid)), "degree": max_degree} 
                for uid in most_connected
            ]
        else:
            summary['most_connected_users'] = []
            
        return jsonify({"status": "success", "stats": summary})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/users", methods=["POST", "DELETE"])
def manage_users():
    """افزودن و حذف کاربر"""
    data = request.json
    uid = parse_id(data.get("id"))
    
    if request.method == "POST":
        try:
            new_user = User(id=uid)
            new_user.name = data.get("name", str(uid))
            graph.add_user(new_user)
            save_data()
            return jsonify({"status": "success", "message": f"کاربر {new_user.name} ایجاد شد."})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    elif request.method == "DELETE":
        try:
            graph.remove_user(uid)
            save_data()
            return jsonify({"status": "success", "message": "کاربر حذف شد."})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/edges", methods=["POST", "DELETE"])
def manage_edges():
    """افزودن و حذف دوستی/رابطه"""
    data = request.json
    source = parse_id(data.get("source"))
    target = parse_id(data.get("target"))
    
    if request.method == "POST":
        try:
            graph.add_edge(source, target)
            save_data()
            return jsonify({"status": "success", "message": "رابطه با موفقیت ایجاد شد."})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    elif request.method == "DELETE":
        try:
            graph.remove_edge(source, target)
            save_data()
            return jsonify({"status": "success", "message": "رابطه با موفقیت قطع شد."})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/friends/<user_id>", methods=["GET"])
def get_friends(user_id):
    """لیست دوستان یک کاربر خاص"""
    try:
        user_id = parse_id(user_id)
        friends = graph.get_neighbors(user_id)
        result = [{"id": f, "name": getattr(graph.get_user(f), 'name', str(f))} for f in friends]
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/recommend/<user_id>", methods=["GET"])
def recommend_friends(user_id):
    """پیشنهاد دوست با استفاده از دوستان مشترک"""
    try:
        user_id = parse_id(user_id)
        rec = Recommendation(graph)
        recommendations = rec.recommend(user_id, limit=5)
        
        result = [{"id": u.id, "name": getattr(u, 'name', str(u.id)), "score": score} for u, score in recommendations]
        return jsonify({"status": "success", "recommendations": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/distances/<user_id>", methods=["GET"])
def get_distances(user_id):
    """فاصله یک کاربر تا سایر کاربران (تحلیل BFS)"""
    try:
        user_id = parse_id(user_id)
        bfs = BFS(graph)
        distances_raw = bfs.distance_to_all(user_id)
        formatted_distances = bfs.format_distances(distances_raw)
        return jsonify({"status": "success", "distances": formatted_distances})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/path/<u1>/<u2>", methods=["GET"])
def get_shortest_path(u1, u2):
    """پیدا کردن کوتاه‌ترین مسیر بین دو کاربر"""
    try:
        u1, u2 = parse_id(u1), parse_id(u2)
        bfs = BFS(graph)
        path_obj = bfs.shortest_path(u1, u2)
        formatted = bfs.format_path(path_obj)
        return jsonify({"status": "success", "path": formatted})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/mutual/<u1>/<u2>", methods=["GET"])
def get_mutual_friends(u1, u2):
    """دوستان مشترک بین دو کاربر"""
    try:
        u1, u2 = parse_id(u1), parse_id(u2)
        n1 = graph.get_neighbors(u1)
        n2 = graph.get_neighbors(u2)
        mutual = n1.intersection(n2)
        
        result = [{"id": mid, "name": getattr(graph.get_user(mid), 'name', str(mid))} for mid in mutual]
        return jsonify({"status": "success", "mutual": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/connection/<u1>/<u2>", methods=["GET"])
def check_connection(u1, u2):
    """بررسی اینکه آیا دو کاربر مستقیماً دوست هستند یا خیر"""
    try:
        u1, u2 = parse_id(u1), parse_id(u2)
        connected = graph.has_edge(u1, u2)
        return jsonify({"status": "success", "connected": connected})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/groups", methods=["GET"])
def get_network_groups():
    """لیست کردن تمام کلاسترها و گروه‌های دوستی (تحلیل DFS)"""
    try:
        dfs = DFS(graph)
        components = dfs.connected_components()
        formatted = dfs.format_components(components)
        return jsonify({"status": "success", "groups": formatted})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    """آپلود دیتاست و اختصاص خودکار آیدی عددی به اسامی متنی"""
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "فایلی ارسال نشده است."}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "فایلی انتخاب نشده است."}), 400
        
    try:
        content = file.read().decode('utf-8').splitlines()
        
        # پیدا کردن بزرگترین آیدی فعلی در گراف برای شروع شماره گذاری جدید
        current_max_id = 0
        for user_id in graph.user_ids():
            try:
                num = int(user_id)
                if num > current_max_id:
                    current_max_id = num
            except ValueError:
                pass
                
        name_to_id = {}
        added_users = 0
        added_edges = 0
        
        for line in content:
            parts = line.strip().split()
            if not parts:
                continue
                
            # ساخت کاربران
            for part in parts:
                if part not in name_to_id:
                    current_max_id += 1
                    name_to_id[part] = current_max_id
                    
                    new_user = User(id=current_max_id)
                    new_user.name = part
                    graph.add_user(new_user)
                    added_users += 1
                    
            # ساخت رابطه
            if len(parts) >= 2:
                id1 = name_to_id[parts[0]]
                id2 = name_to_id[parts[1]]
                
                if not graph.has_edge(id1, id2):
                    graph.add_edge(id1, id2)
                    added_edges += 1
                    
        save_data()
        return jsonify({
            "status": "success", 
            "message": f"پردازش موفق: {added_users} کاربر جدید و {added_edges} رابطه به گراف اضافه شد."
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطا در پردازش فایل: {str(e)}"}), 500

@app.route("/api/reset", methods=["POST"])
def reset_graph():
    """پاکسازی کامل گراف و دیتابیس"""
    try:
        graph.clear()
        save_data()
        return jsonify({"status": "success", "message": "دیتابیس شبکه با موفقیت پاکسازی شد."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    load_data()  # بارگذاری دیتا در هنگام شروع سرور
    app.run(debug=True)