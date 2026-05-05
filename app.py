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

# 2. API สำหรับให้ JavaScript ดึงข้อมูลผู้ใช้งาน
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, fullname, role, TO_CHAR(expire_date, 'YYYY-MM-DD') FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    users = [{"user": r[0], "pass": r[1], "name": r[2], "role": r[3], "expire_date": r[4]} for r in rows]
    return jsonify(users)

if __name__ == '__main__':
    # รันเว็บเซิร์ฟเวอร์ในเครื่องเพื่อทดสอบ
    app.run(host='0.0.0.0', port=5000, debug=True)