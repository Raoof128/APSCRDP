#!/usr/bin/env python3
"""
Intentionally Vulnerable Flask Application
FOR SECURITY TESTING PURPOSES ONLY

This application contains multiple OWASP Top 10 vulnerabilities:
- SQL Injection
- Cross-Site Scripting (XSS)
- Hardcoded Credentials
- Insecure Deserialization
- Command Injection
- Path Traversal
- Weak Cryptography
- Broken Access Control
"""

from flask import Flask, request, render_template_string, redirect
import sqlite3
import pickle
import os
import subprocess
import hashlib

app = Flask(__name__)

# VULNERABILITY: Hardcoded Credentials (CWE-798)
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdefghijklmnop"
SECRET_KEY = "supersecretkey"

app.config['SECRET_KEY'] = SECRET_KEY


def get_db_connection():
    """Database connection with hardcoded credentials"""
    conn = sqlite3.connect('users.db')
    return conn


@app.route('/')
def index():
    return '''
    <h1>Vulnerable Flask App - Security Testing</h1>
    <ul>
        <li><a href="/search?q=test">Search (SQL Injection)</a></li>
        <li><a href="/greet?name=User">Greet (XSS)</a></li>
        <li><a href="/file?path=test.txt">Read File (Path Traversal)</a></li>
        <li><a href="/ping?host=localhost">Ping (Command Injection)</a></li>
    </ul>
    '''


@app.route('/search')
def search():
    """VULNERABILITY: SQL Injection (CWE-89)"""
    query = request.args.get('q', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vulnerable SQL query - directly interpolating user input
    sql = f"SELECT * FROM users WHERE username = '{query}'"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()

        return {'results': results, 'query': sql}
    except Exception as e:
        return {'error': str(e)}


@app.route('/greet')
def greet():
    """VULNERABILITY: Cross-Site Scripting (CWE-79)"""
    name = request.args.get('name', 'Guest')

    # Vulnerable template rendering - no escaping
    template = f'''
    <html>
        <body>
            <h1>Hello, {name}!</h1>
            <p>Welcome to our site</p>
        </body>
    </html>
    '''

    return render_template_string(template)


@app.route('/file')
def read_file():
    """VULNERABILITY: Path Traversal (CWE-22)"""
    file_path = request.args.get('path', 'default.txt')

    # Vulnerable - no path validation
    try:
        full_path = os.path.join('/var/www/files/', file_path)
        with open(full_path, 'r') as f:
            content = f.read()
        return {'content': content}
    except Exception as e:
        return {'error': str(e)}


@app.route('/ping')
def ping():
    """VULNERABILITY: Command Injection (CWE-78)"""
    host = request.args.get('host', 'localhost')

    # Vulnerable - directly executing shell command with user input
    try:
        result = subprocess.check_output(
            f'ping -c 1 {host}',
            shell=True,  # Dangerous!
            text=True
        )
        return {'output': result}
    except Exception as e:
        return {'error': str(e)}


@app.route('/deserialize', methods=['POST'])
def deserialize():
    """VULNERABILITY: Insecure Deserialization (CWE-502)"""
    data = request.data

    # Vulnerable - unpickling untrusted data
    try:
        obj = pickle.loads(data)
        return {'deserialized': str(obj)}
    except Exception as e:
        return {'error': str(e)}


@app.route('/hash')
def hash_password():
    """VULNERABILITY: Weak Cryptography (CWE-327)"""
    password = request.args.get('password', '')

    # Vulnerable - using MD5 for password hashing
    hashed = hashlib.md5(password.encode()).hexdigest()

    return {'hash': hashed, 'algorithm': 'MD5'}


@app.route('/admin')
def admin():
    """VULNERABILITY: Broken Access Control (CWE-285)"""
    # No authentication check!

    return {
        'message': 'Admin panel access granted',
        'sensitive_data': {
            'users': ['admin', 'user1', 'user2'],
            'api_keys': [API_KEY],
            'database_password': DATABASE_PASSWORD
        }
    }


@app.route('/redirect')
def open_redirect():
    """VULNERABILITY: Open Redirect (CWE-601)"""
    url = request.args.get('url', 'https://example.com')

    # Vulnerable - no URL validation
    return redirect(url)


def init_db():
    """Initialize database with sample data"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')

    # Insert sample data
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@example.com')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (2, 'user', 'password', 'user@example.com')"
    )

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()

    # VULNERABILITY: Debug mode enabled in production (CWE-489)
    app.run(
        host='0.0.0.0',  # Binding to all interfaces
        port=5000,
        debug=True  # Never use debug=True in production!
    )
