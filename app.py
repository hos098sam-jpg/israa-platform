from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# تحديد مسار قاعدة البيانات عشان تشتغل على السيرفر صح
DB_PATH = os.path.join(os.getcwd(), 'israa.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # جدول الدروس (العنوان، رابط الفيديو، رابط الـ PDF)
    cursor.execute('''CREATE TABLE IF NOT EXISTS lessons 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT, 
                       video_url TEXT, 
                       pdf_url TEXT)''')
    conn.commit()
    conn.close()

# واجهة الصفحة الرئيسية (الستايل بلون غامق واحترافي)
HOME_HTML = """
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة الإسراء التعليمية</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: auto; }
        h1 { color: #00d4ff; }
        .card { background: #1e1e1e; padding: 20px; margin: 15px 0; border-radius: 12px; border: 1px solid #333; transition: 0.3s; }
        .card:hover { border-color: #00d4ff; box-shadow: 0 0 10px rgba(0,212,255,0.2); }
        .btn { background: #00d4ff; color: #000; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; }
        .admin-link { color: #555; text-decoration: none; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة الإسراء التعليمية 📚</h1>
        <p>مرحباً بك يا بطل في دروس التاريخ للثانوية العامة</p>
        <hr style="border: 0.5px solid #333;">
        
        {% if lessons %}
            {% for l in lessons %}
            <div class="card">
                <h3>{{ l[1] }}</h3>
                <a href="{{ l[2] }}" target="_blank" class="btn">مشاهدة الفيديو</a>
                {% if l[3] %}
                <a href="{{ l[3] }}" target="_blank" class="btn" style="background:#ff9800;">تحميل PDF</a>
                {% endif %}
            </div>
            {% endfor %}
        {% else %}
            <p>لا يوجد دروس مضافة حالياً.</p>
        {% endif %}
        
        <br><br>
        <a href="/admin" class="admin-link">لوحة التحكم</a>
    </div>
</body>
</html>
"""

# واجهة لوحة التحكم
ADMIN_HTML = """
<html dir="rtl">
<body style="text-align:center; padding:50px; font-family:Arial;">
    <h2>إضافة درس جديد للمنصة</h2>
    <form action="/add" method="POST" style="display:inline-block; text-align:right;">
        <label>عنوان الدرس:</label><br>
        <input name="title" required style="width:300px; padding:8px;"><br><br>
        <label>رابط فيديو يوتيوب:</label><br>
        <input name="video" required style="width:300px; padding:8px;"><br><br>
        <label>رابط ملف الـ PDF (اختياري):</label><br>
        <input name="pdf" style="width:300px; padding:8px;"><br><br>
        <button type="submit" style="padding:10px 20px; cursor:pointer; background:#28a745; color:white; border:none; border-radius:5px;">نشر الآن</button>
    </form>
    <br><br><a href="/">العودة للرئيسية</a>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()
    conn.close()
    return render_template_string(HOME_HTML, lessons=lessons)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_HTML)

@app.route('/add', methods=['POST'])
def add():
    t = request.form.get('title')
    v = request.form.get('video')
    p = request.form.get('pdf')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lessons (title, video_url, pdf_url) VALUES (?, ?, ?)", (t, v, p))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run()
