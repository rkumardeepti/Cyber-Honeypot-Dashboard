# import sqlite3
# from datetime import datetime
# import requests

# class HoneypotDB:
#     def __init__(self, db_name="honeypot.db"):
#         self.db_name = db_name
#         self.create_table()
    
#     def create_table(self):
#         """Create attempts table with location fields"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS login_attempts (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 ip_address TEXT,
#                 username TEXT,
#                 password TEXT,
#                 user_agent TEXT,
#                 country TEXT,
#                 city TEXT,
#                 isp TEXT,
#                 attempt_count INTEGER DEFAULT 1,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
        
#         conn.commit()
#         conn.close()
    
#     def get_ip_geolocation(self, ip):
#         """Get geolocation data for an IP address"""
#         # Skip local IPs
#         if ip.startswith('127.') or ip.startswith('192.168.') or ip == '::1':
#             return {'country': 'Local', 'city': 'Local Network', 'isp': 'Local'}
        
#         try:
#             # Using free ip-api.com (no API key needed)
#             response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
#             data = response.json()
            
#             if data.get('status') == 'success':
#                 return {
#                     'country': data.get('country', 'Unknown'),
#                     'city': data.get('city', 'Unknown'),
#                     'isp': data.get('isp', 'Unknown')
#                 }
#             else:
#                 return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
#         except:
#             return {'country': 'Error', 'city': 'Error', 'isp': 'Error'}
    
#     def get_ip_attempt_count(self, ip):
#         """Get number of attempts from this IP in last hour"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT COUNT(*) FROM login_attempts 
#             WHERE ip_address = ? AND timestamp >= datetime('now', '-1 hour')
#         ''', (ip,))
        
#         count = cursor.fetchone()[0]
#         conn.close()
#         return count
    
#     def log_attempt(self, ip, username, password, user_agent):
#         """Log a failed login attempt with geolocation"""
#         # Get geolocation
#         location = self.get_ip_geolocation(ip)
        
#         # Get attempt count
#         attempt_count = self.get_ip_attempt_count(ip) + 1
        
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             INSERT INTO login_attempts 
#             (ip_address, username, password, user_agent, country, city, isp, attempt_count)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (ip, username, password, user_agent, 
#               location['country'], location['city'], location['isp'], attempt_count))
        
#         conn.commit()
#         conn.close()
        
#         # Check for alert condition
#         if attempt_count >= 5:
#             self.trigger_alert(ip, attempt_count, username)
        
#         return location
    
#     def trigger_alert(self, ip, count, username):
#         """Trigger alert for suspicious activity"""
#         # This will be displayed in dashboard
#         print(f"⚠️ ALERT: {count} attempts from {ip} in last hour! Last username: {username}")
    
#     def get_all_attempts(self, limit=100):
#         """Get all login attempts with location data"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT id, ip_address, username, password, user_agent, 
#                    country, city, isp, attempt_count,
#                    datetime(timestamp, 'localtime') as timestamp
#             FROM login_attempts 
#             ORDER BY timestamp DESC
#             LIMIT ?
#         ''', (limit,))
        
#         attempts = cursor.fetchall()
#         conn.close()
        
#         return attempts
    
#     def get_suspicious_ips(self):
#         """Get IPs with high attempt counts"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT ip_address, MAX(attempt_count) as attempts, 
#                    country, city, MAX(timestamp) as last_attempt
#             FROM login_attempts 
#             WHERE attempt_count >= 3
#             GROUP BY ip_address
#             ORDER BY attempts DESC
#             LIMIT 10
#         ''')
        
#         suspicious = cursor.fetchall()
#         conn.close()
#         return suspicious
    
#     def get_statistics(self):
#         """Get enhanced statistics"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         # Total attempts
#         cursor.execute("SELECT COUNT(*) FROM login_attempts")
#         total = cursor.fetchone()[0]
        
#         # Unique IPs
#         cursor.execute("SELECT COUNT(DISTINCT ip_address) FROM login_attempts")
#         unique_ips = cursor.fetchone()[0]
        
#         # Top usernames
#         cursor.execute('''
#             SELECT username, COUNT(*) as count 
#             FROM login_attempts 
#             GROUP BY username 
#             ORDER BY count DESC 
#             LIMIT 5
#         ''')
#         top_usernames = cursor.fetchall()
        
#         # Attempts in last hour
#         cursor.execute('''
#             SELECT COUNT(*) FROM login_attempts 
#             WHERE timestamp >= datetime('now', '-1 hour')
#         ''')
#         last_hour = cursor.fetchone()[0]
        
#         # Countries attacking
#         cursor.execute('''
#             SELECT country, COUNT(*) as count 
#             FROM login_attempts 
#             WHERE country NOT IN ('Local', 'Unknown', 'Error')
#             GROUP BY country 
#             ORDER BY count DESC 
#             LIMIT 5
#         ''')
#         top_countries = cursor.fetchall()
        
#         # Alerts (suspicious IPs)
#         alerts = self.get_suspicious_ips()
        
#         conn.close()
        
#         return {
#             'total': total,
#             'unique_ips': unique_ips,
#             'top_usernames': top_usernames,
#             'last_hour': last_hour,
#             'top_countries': top_countries,
#             'alerts': alerts
#         }

# import sqlite3
# from datetime import datetime
# import requests

# class HoneypotDB:
#     def __init__(self, db_name="honeypot.db"):
#         self.db_name = db_name
#         self.create_table()
    
#     def create_table(self):
#         """Create attempts table with proper timestamp handling"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS login_attempts (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 ip_address TEXT,
#                 username TEXT,
#                 password TEXT,
#                 user_agent TEXT,
#                 country TEXT DEFAULT 'Unknown',
#                 city TEXT DEFAULT 'Unknown',
#                 isp TEXT DEFAULT 'Unknown',
#                 attempt_count INTEGER DEFAULT 1,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
        
#         conn.commit()
#         conn.close()
    
#     def get_ip_geolocation(self, ip):
#         """Get geolocation data for an IP address"""
#         if ip.startswith('127.') or ip.startswith('192.168.') or ip == '::1' or ip.startswith('10.'):
#             return {'country': 'Local', 'city': 'Local Network', 'isp': 'Local'}
        
#         try:
#             response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
#             data = response.json()
            
#             if data.get('status') == 'success':
#                 return {
#                     'country': data.get('country', 'Unknown'),
#                     'city': data.get('city', 'Unknown'),
#                     'isp': data.get('isp', 'Unknown')
#                 }
#             return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
#         except:
#             return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
    
#     def get_ip_attempt_count(self, ip):
#         """Get number of attempts from this IP in last hour"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT COUNT(*) FROM login_attempts 
#             WHERE ip_address = ? AND timestamp >= datetime('now', '-1 hour')
#         ''', (ip,))
        
#         count = cursor.fetchone()[0]
#         conn.close()
#         return count
    
#     def log_attempt(self, ip, username, password, user_agent):
#         """Log a failed login attempt with real timestamp"""
#         location = self.get_ip_geolocation(ip)
#         attempt_count = self.get_ip_attempt_count(ip) + 1
        
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             INSERT INTO login_attempts 
#             (ip_address, username, password, user_agent, country, city, isp, attempt_count, timestamp)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
#         ''', (ip, username, password, user_agent, 
#               location['country'], location['city'], location['isp'], attempt_count))
        
#         conn.commit()
#         conn.close()
        
#         if attempt_count >= 5:
#             print(f"⚠️ ALERT: {attempt_count} attempts from {ip} in last hour!")
        
#         return location
    
#     def get_all_attempts(self, limit=100):
#         """Get all login attempts with proper timestamps"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT id, ip_address, username, password, user_agent, 
#                    country, city, isp, attempt_count,
#                    datetime(timestamp, 'localtime') as timestamp
#             FROM login_attempts 
#             ORDER BY timestamp DESC
#             LIMIT ?
#         ''', (limit,))
        
#         attempts = cursor.fetchall()
#         conn.close()
#         return attempts
    
#     def get_suspicious_ips(self):
#         """Get IPs with high attempt counts"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute('''
#             SELECT ip_address, MAX(attempt_count) as attempts, 
#                    country, city, MAX(timestamp) as last_attempt
#             FROM login_attempts 
#             WHERE attempt_count >= 3
#             GROUP BY ip_address
#             ORDER BY attempts DESC
#             LIMIT 10
#         ''')
        
#         suspicious = cursor.fetchall()
#         conn.close()
#         return suspicious
    
#     def get_statistics(self):
#         """Get statistics with real data"""
#         conn = sqlite3.connect(self.db_name)
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT COUNT(*) FROM login_attempts")
#         total = cursor.fetchone()[0]
        
#         cursor.execute("SELECT COUNT(DISTINCT ip_address) FROM login_attempts")
#         unique_ips = cursor.fetchone()[0]
        
#         cursor.execute('''
#             SELECT username, COUNT(*) as count 
#             FROM login_attempts 
#             WHERE username IS NOT NULL AND username != '' AND username != 'ADMIN_PANEL_ACCESS'
#             GROUP BY username 
#             ORDER BY count DESC 
#             LIMIT 5
#         ''')
#         top_usernames = cursor.fetchall()
        
#         cursor.execute('''
#             SELECT COUNT(*) FROM login_attempts 
#             WHERE timestamp >= datetime('now', '-1 hour')
#         ''')
#         last_hour = cursor.fetchone()[0]
        
#         cursor.execute('''
#             SELECT country, COUNT(*) as count 
#             FROM login_attempts 
#             WHERE country NOT IN ('Local', 'Unknown', 'Error') AND country IS NOT NULL
#             GROUP BY country 
#             ORDER BY count DESC 
#             LIMIT 5
#         ''')
#         top_countries = cursor.fetchall()
        
#         alerts = self.get_suspicious_ips()
        
#         conn.close()
        
#         return {
#             'total': total,
#             'unique_ips': unique_ips,
#             'top_usernames': top_usernames if top_usernames else [],
#             'last_hour': last_hour,
#             'top_countries': top_countries if top_countries else [],
#             'alerts': alerts if alerts else []
#         }

import sqlite3
from datetime import datetime
import requests

class HoneypotDB:
    def __init__(self, db_name="honeypot.db"):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Create attempts table with proper timestamp handling"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                username TEXT,
                password TEXT,
                user_agent TEXT,
                country TEXT DEFAULT 'Unknown',
                city TEXT DEFAULT 'Unknown',
                isp TEXT DEFAULT 'Unknown',
                attempt_count INTEGER DEFAULT 1,
                timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database created with proper timestamp support")
    
    def get_ip_geolocation(self, ip):
        """Get geolocation data for an IP address"""
        if ip.startswith('127.') or ip.startswith('192.168.') or ip == '::1' or ip.startswith('10.'):
            return {'country': 'Local', 'city': 'Local Network', 'isp': 'Local'}
        
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'isp': data.get('isp', 'Unknown')
                }
            return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
        except:
            return {'country': 'Unknown', 'city': 'Unknown', 'isp': 'Unknown'}
    
    def get_ip_attempt_count(self, ip):
        """Get number of attempts from this IP in last hour"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM login_attempts 
            WHERE ip_address = ? AND timestamp >= datetime('now', '-1 hour', 'localtime')
        ''', (ip,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def log_attempt(self, ip, username, password, user_agent):
        """Log a failed login attempt with REAL timestamp"""
        location = self.get_ip_geolocation(ip)
        attempt_count = self.get_ip_attempt_count(ip) + 1
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Get current timestamp in proper format
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO login_attempts 
            (ip_address, username, password, user_agent, country, city, isp, attempt_count, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ip, username, password, user_agent, 
              location['country'], location['city'], location['isp'], attempt_count, current_time))
        
        conn.commit()
        conn.close()
        
        print(f"[LOG] {current_time} - {ip} tried {username}:{password}")
        
        if attempt_count >= 5:
            print(f"⚠️ ALERT: {attempt_count} attempts from {ip} in last hour!")
        
        return location
    
    def get_all_attempts(self, limit=100):
        """Get all login attempts with REAL timestamps"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, ip_address, username, password, user_agent, 
                   country, city, isp, attempt_count,
                   timestamp
            FROM login_attempts 
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        attempts = cursor.fetchall()
        conn.close()
        return attempts
    
    def get_suspicious_ips(self):
        """Get IPs with high attempt counts"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ip_address, MAX(attempt_count) as attempts, 
                   country, city, MAX(timestamp) as last_attempt
            FROM login_attempts 
            WHERE attempt_count >= 3
            GROUP BY ip_address
            ORDER BY attempts DESC
            LIMIT 10
        ''')
        
        suspicious = cursor.fetchall()
        conn.close()
        return suspicious
    
    def get_statistics(self):
        """Get statistics with real data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM login_attempts")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT ip_address) FROM login_attempts")
        unique_ips = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT username, COUNT(*) as count 
            FROM login_attempts 
            WHERE username IS NOT NULL AND username != '' AND username != 'ADMIN_PANEL_ACCESS'
            GROUP BY username 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        top_usernames = cursor.fetchall()
        
        cursor.execute('''
            SELECT COUNT(*) FROM login_attempts 
            WHERE timestamp >= datetime('now', '-1 hour', 'localtime')
        ''')
        last_hour = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT country, COUNT(*) as count 
            FROM login_attempts 
            WHERE country NOT IN ('Local', 'Unknown', 'Error') AND country IS NOT NULL
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        top_countries = cursor.fetchall()
        
        alerts = self.get_suspicious_ips()
        
        conn.close()
        
        return {
            'total': total,
            'unique_ips': unique_ips,
            'top_usernames': top_usernames if top_usernames else [],
            'last_hour': last_hour,
            'top_countries': top_countries if top_countries else [],
            'alerts': alerts if alerts else []
        }