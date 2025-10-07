from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["PREFERRED_URL_SCHEME"] = "https"
DB_PATH = os.environ.get("DB_PATH", "smartoffice.db")

# OAuth configuration - Must be set as environment variables
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    print("WARNING: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables must be set for Gmail integration")

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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gmail_tokens (
            user_id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            refresh_token TEXT,
            token_uri TEXT,
            token_expiry TEXT,
            scopes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

def get_user_gmail_credentials(user_id):
    """Get Gmail credentials from database for a specific user"""
    conn = get_db()
    token_row = conn.execute("SELECT * FROM gmail_tokens WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if not token_row:
        return None
    
    from datetime import datetime
    expiry = None
    if token_row['token_expiry']:
        try:
            expiry = datetime.fromisoformat(token_row['token_expiry'])
        except:
            pass
    
    creds = Credentials(
        token=token_row['token'],
        refresh_token=token_row['refresh_token'],
        token_uri=token_row['token_uri'],
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=json.loads(token_row['scopes']) if token_row['scopes'] else [],
        expiry=expiry
    )
    
    # Refresh token if expired
    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
        save_user_gmail_credentials(user_id, creds)
    
    return creds

def save_user_gmail_credentials(user_id, credentials):
    """Save Gmail credentials to database for a specific user"""
    conn = get_db()
    
    expiry_str = None
    if credentials.expiry:
        expiry_str = credentials.expiry.isoformat()
    
    conn.execute("""
        INSERT OR REPLACE INTO gmail_tokens 
        (user_id, token, refresh_token, token_uri, token_expiry, scopes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        credentials.token,
        credentials.refresh_token,
        credentials.token_uri,
        expiry_str,
        json.dumps(credentials.scopes) if credentials.scopes else '[]'
    ))
    conn.commit()
    conn.close()

def get_gmail_service(user_id):
    """Get authenticated Gmail service for a specific user"""
    creds = get_user_gmail_credentials(user_id)
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

@app.route("/debug-oauth")
@login_required
def debug_oauth():
    """Debug endpoint to show OAuth configuration"""
    redirect_uri = url_for('oauth2callback', _external=True)
    return f"""
    <h2>OAuth Debug Info</h2>
    <p><strong>Client ID:</strong> {GOOGLE_CLIENT_ID or 'NOT SET'}</p>
    <p><strong>Client Secret:</strong> {'SET' if GOOGLE_CLIENT_SECRET else 'NOT SET'}</p>
    <p><strong>Redirect URI:</strong> {redirect_uri}</p>
    <p><strong>Scopes:</strong> {', '.join(SCOPES)}</p>
    <hr>
    <p><strong>Instructions:</strong> Copy the Redirect URI above and add it to your Google Cloud Console OAuth 2.0 Client ID configuration under "Authorized redirect URIs"</p>
    <p><a href="/email">Back to Email</a></p>
    """

@app.route("/gmail-authorize")
@login_required
def gmail_authorize():
    """Start OAuth flow for Gmail"""
    user = current_user()
    
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        flash("Gmail integration is not configured. Please contact administrator.", "danger")
        return redirect(url_for('email'))
    
    redirect_uri = url_for('oauth2callback', _external=True)
    print(f"[OAuth] Starting flow with redirect_uri: {redirect_uri}")
    print(f"[OAuth] Client ID: {GOOGLE_CLIENT_ID[:20]}...")
    
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        print(f"[OAuth] Authorization URL generated: {authorization_url[:100]}...")
        session['oauth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        print(f"[OAuth ERROR] Failed to start authorization: {e}")
        flash(f"OAuth configuration error: {str(e)}", "danger")
        return redirect(url_for('email'))

@app.route("/oauth2callback")
def oauth2callback():
    """Handle OAuth callback from Google"""
    user = current_user()
    if not user:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    
    state = session.get('oauth_state')
    redirect_uri = url_for('oauth2callback', _external=True)
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=state,
        redirect_uri=redirect_uri
    )
    
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    save_user_gmail_credentials(user['id'], credentials)
    
    flash("Gmail connected successfully!", "success")
    return redirect(url_for('email'))

@app.route("/email")
@login_required
def email():
    user = current_user()
    gmail_service = get_gmail_service(user['id'])
    
    if not gmail_service:
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
        print(f"Error fetching emails: {str(e)}")
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
