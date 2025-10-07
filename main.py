from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DB_PATH = os.environ.get("DB_PATH", "smartoffice.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

def get_gmail_credentials():
    """Get Gmail credentials from Replit Connectors"""
    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME")
    repl_identity = os.environ.get("REPL_IDENTITY")
    web_repl_renewal = os.environ.get("WEB_REPL_RENEWAL")
    
    if not hostname:
        return None
    
    x_replit_token = None
    if repl_identity:
        x_replit_token = f"repl {repl_identity}"
    elif web_repl_renewal:
        x_replit_token = f"depl {web_repl_renewal}"
    
    if not x_replit_token:
        return None
    
    try:
        response = requests.get(
            f"https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-mail",
            headers={
                "Accept": "application/json",
                "X-Replit-Token": x_replit_token
            }
        )
        
        if response.status_code != 200:
            print(f"Connector API returned status {response.status_code}")
            return None
        
        data = response.json()
        if not data or "items" not in data or len(data["items"]) == 0:
            print("No Gmail connection found in connector response")
            return None
        
        connection = data["items"][0]
        settings = connection.get("settings", {})
        
        # Try to get access token from settings structure
        access_token = settings.get("access_token")
        if not access_token and "oauth" in settings:
            oauth_data = settings.get("oauth", {})
            credentials = oauth_data.get("credentials", {})
            access_token = credentials.get("access_token")
        
        if not access_token:
            print("No access token found in connection settings")
            return None
        
        # Create credentials with the access token
        creds = Credentials(token=access_token)
        
        return creds
    
    except Exception as e:
        print(f"Error getting Gmail credentials: {e}")
        return None

def get_gmail_service():
    """Get authenticated Gmail service"""
    creds = get_gmail_credentials()
    if not creds:
        return None
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return None

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = get_db()
    user = conn.execute("SELECT id, email, name FROM users WHERE id = ?", (uid,)).fetchone()
    conn.close()
    return user

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return wrapper

@app.route("/")
@login_required
def index():
    user = current_user()
    return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        conn = get_db()
        row = conn.execute("SELECT id, password_hash, name FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if row and check_password_hash(row["password_hash"], password):
            session["user_id"] = row["id"]
            flash("Welcome back!", "success")
            nxt = request.args.get("next") or url_for("index")
            return redirect(nxt)
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or not password:
            flash("All fields are required.", "warning")
            return render_template("register.html", name=name, email=email)
        pw_hash = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)", (email, name, pw_hash))
            conn.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("login"))

@app.route("/email")
@login_required
def email():
    user = current_user()
    gmail_service = get_gmail_service()
    
    if not gmail_service:
        flash("Gmail is not connected. Please reconnect your Gmail account.", "warning")
        return render_template("email.html", user=user, emails=[], connected=False)
    
    try:
        results = gmail_service.users().messages().list(userId='me', maxResults=15).execute()
        messages = results.get('messages', [])
        
        emails = []
        for msg in messages:
            msg_data = gmail_service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
            
            email_info = {
                'id': msg['id'],
                'subject': 'No Subject',
                'sender': 'Unknown',
                'date': 'Unknown',
                'snippet': msg_data.get('snippet', '')
            }
            
            for header in msg_data.get('payload', {}).get('headers', []):
                if header['name'] == 'Subject':
                    email_info['subject'] = header['value']
                elif header['name'] == 'From':
                    email_info['sender'] = header['value']
                elif header['name'] == 'Date':
                    email_info['date'] = header['value']
            
            emails.append(email_info)
        
        return render_template("email.html", user=user, emails=emails, connected=True)
    
    except Exception as e:
        flash(f"Error fetching emails: {str(e)}", "danger")
        return render_template("email.html", user=user, emails=[], connected=False)

@app.route("/calendar")
@login_required
def calendar():
    return render_template("feature.html", title="Calendar", subtitle="Google Calendar integration coming soon…")

@app.route("/reports")
@login_required
def reports():
    return render_template("feature.html", title="Reports", subtitle="Weekly PDF/Word reports will appear here…")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
