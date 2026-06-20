from flask import Flask, render_template, request, jsonify, Response
from database import HoneypotDB
import csv
import io
from datetime import datetime

app = Flask(__name__)
db = HoneypotDB()

@app.route('/')
def login_page():
    """Display the fake login page"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def fake_login():
    """Handle login attempts - always fails but logs everything"""
    # Get client IP address
    ip_address = request.remote_addr
    
    # Check if behind proxy
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For').split(',')[0]
    
    # Get login credentials
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    user_agent = request.headers.get('User-Agent', '')
    
    # Log the attempt with geolocation
    location = db.log_attempt(ip_address, username, password, user_agent)
    
    # Always show error (fake login)
    return render_template('index.html', error="Invalid credentials. Please try again.")

@app.route('/log-admin-action', methods=['POST'])
def log_admin_action():
    """Log admin panel button clicks"""
    import json
    from datetime import datetime
    
    ip_address = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For').split(',')[0]
    
    data = request.get_json()
    action = data.get('action', 'Unknown action')
    
    # Print to terminal for monitoring
    print(f"[ADMIN TRAP] {datetime.now().strftime('%H:%M:%S')} - IP: {ip_address} - Action: {action}")
    
    # Also log to database if you want
    try:
        import sqlite3
        conn = sqlite3.connect('honeypot.db')
        cursor = conn.cursor()
        
        # Create admin_logs table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('INSERT INTO admin_logs (ip_address, action) VALUES (?, ?)', 
                      (ip_address, f"ADMIN: {action}"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database log error: {e}")
    
    return jsonify({'status': 'logged', 'message': 'Action recorded'})

@app.route('/admin')
def fake_admin():
    """Fake admin panel trap - logs access attempts"""
    ip_address = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For').split(',')[0]
    
    # Log admin panel access attempt
    db.log_attempt(ip_address, "ADMIN_PANEL_ACCESS", "N/A", request.headers.get('User-Agent', ''))
    
    # Show fake admin panel (looks real but logs everything)
    return render_template('fake_admin.html')

@app.route('/dashboard')
def dashboard():
    """Admin dashboard to view attempts"""
    attempts = db.get_all_attempts(100)
    stats = db.get_statistics()
    suspicious_ips = db.get_suspicious_ips()
    
    return render_template('dashboard.html', 
                         attempts=attempts, 
                         stats=stats,
                         suspicious_ips=suspicious_ips)

@app.route('/api/attempts')
def api_attempts():
    """JSON API for attempts with REAL timestamps"""
    attempts = db.get_all_attempts(50)
    
    data = []
    for attempt in attempts:
        # attempt[0]=id, [1]=ip, [2]=username, [3]=password, [4]=user_agent
        # [5]=country, [6]=city, [7]=isp, [8]=attempt_count, [9]=timestamp
        timestamp = attempt[9] if attempt[9] and attempt[9] != 'Local' else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data.append({
            'id': attempt[0],
            'ip': attempt[1],
            'username': attempt[2] if attempt[2] else '(empty)',
            'password': attempt[3] if attempt[3] else '(empty)',
            'country': attempt[5] if attempt[5] else 'Unknown',
            'city': attempt[6] if attempt[6] else 'Unknown',
            'timestamp': timestamp
        })
    
    return jsonify(data)
    
@app.route('/api/stats')
def api_stats():
    """JSON API for statistics"""
    stats = db.get_statistics()
    
    # Convert tuple data to dictionary format
    stats['top_usernames'] = [
        {'username': u[0] if u[0] else '(empty)', 'count': u[1]} 
        for u in stats['top_usernames']
    ]
    
    stats['top_countries'] = [
        {'country': c[0] if c[0] else 'Unknown', 'count': c[1]} 
        for c in stats['top_countries']
    ]
    
    stats['alerts'] = [
        {
            'ip': a[0], 
            'attempts': a[1], 
            'country': a[2] if a[2] else 'Unknown',
            'city': a[3] if a[3] else 'Unknown'
        } 
        for a in stats['alerts']
    ]
    
    return jsonify(stats)

@app.route('/export/csv')
def export_csv():
    """Export all logs to CSV file"""
    attempts = db.get_all_attempts(limit=1000)  # Get last 1000 attempts
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['ID', 'IP Address', 'Username', 'Password', 'User Agent', 
                    'Country', 'City', 'ISP', 'Attempt Count', 'Timestamp'])
    
    # Write data
    for attempt in attempts:
        writer.writerow([
            attempt[0], attempt[1], attempt[2], attempt[3], attempt[4],
            attempt[5], attempt[6], attempt[7], attempt[8], attempt[9]
        ])
    
    # Return CSV file
    output.seek(0)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=honeypot_logs_{timestamp}.csv'}
    )

if __name__ == '__main__':
    print("="*50)
    print("🧲 HONEYPOT DASHBOARD - ADVANCED EDITION")
    print("="*50)
    print("📍 Fake Login Page: http://127.0.0.1:5000")
    print("🎭 Fake Admin Panel: http://127.0.0.1:5000/admin")
    print("📊 Admin Dashboard: http://127.0.0.1:5000/dashboard")
    print("📥 Export Logs: http://127.0.0.1:5000/export/csv")
    print("="*50)
    print("⚠️  All login attempts will be logged with geolocation!")
    print("🚨 Alerts trigger after 5 attempts from same IP in 1 hour")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)

