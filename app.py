from flask import Flask, render_template, request, jsonify
import psycopg2

# บังคับให้ Flask รู้ว่าโฟลเดอร์ปัจจุบันคือโฟลเดอร์ที่มี INDEX.html
app = Flask(__name__, template_folder='.', static_folder='.')

# ใส่ Connection String ของ Neon DB ลงไป
DB_URL = "postgresql://neondb_owner:npg_e0jiluRCOaS2@ep-silent-resonance-aofq4y3u-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

# 1. หน้าแรกของเว็บ (เวลาคนพิมพ์ URL เข้ามา)
@app.route('/')
def home():
    return render_template('INDEX.html')

# API บันทึกข้อมูล User (จากหน้า Admin)
@app.route('/api/users', methods=['POST'])
def save_users():
    conn = None
    cursor = None
    try:
        new_users_list = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        
        for u in new_users_list:
            expire = u.get('expire_date', '2099-12-31')
            if not expire: expire = '2099-12-31'
            cursor.execute('''
                INSERT INTO users (username, password, fullname, role, expire_date) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (u['user'], u['pass'], u['name'], u['role'], expire))
            
        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        # บังคับปิดการเชื่อมต่อทุกครั้ง ป้องกัน Neon DB ค้าง
        if cursor: cursor.close()
        if conn: conn.close()
