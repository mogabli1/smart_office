from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, json, requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timezone, timedelta
from openai import OpenAI

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

# OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("INFO: OPENAI_API_KEY not set - AI features will be disabled")

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
    
    refresh_token = credentials.refresh_token
    if not refresh_token:
        existing = conn.execute(
            "SELECT refresh_token FROM gmail_tokens WHERE user_id = ?", 
            (user_id,)
        ).fetchone()
        if existing:
            refresh_token = existing['refresh_token']
    
    conn.execute("""
        INSERT OR REPLACE INTO gmail_tokens 
        (user_id, token, refresh_token, token_uri, token_expiry, scopes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        credentials.token,
        refresh_token,
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

def get_calendar_access_token():
    """Get Google Calendar access token from Replit connector"""
    hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
    repl_identity = os.environ.get('REPL_IDENTITY')
    web_repl_renewal = os.environ.get('WEB_REPL_RENEWAL')
    
    x_replit_token = None
    if repl_identity:
        x_replit_token = 'repl ' + repl_identity
    elif web_repl_renewal:
        x_replit_token = 'depl ' + web_repl_renewal
    
    if not hostname or not x_replit_token:
        return None
    
    try:
        url = f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-calendar'
        headers = {
            'Accept': 'application/json',
            'X_REPLIT_TOKEN': x_replit_token
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            return None
        
        connection_settings = items[0]
        access_token = connection_settings.get('settings', {}).get('access_token')
        
        if not access_token:
            access_token = connection_settings.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
        
        return access_token
    except Exception as e:
        print(f"Error fetching calendar access token: {e}")
        return None

def get_calendar_service():
    """Get authenticated Google Calendar service using Replit connector"""
    access_token = get_calendar_access_token()
    
    if not access_token:
        return None
    
    try:
        from google.oauth2.credentials import Credentials as OAuth2Credentials
        creds = OAuth2Credentials(token=access_token)
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Calendar service: {e}")
        return None

def analyze_email_priority(subject, sender, snippet):
    """
    Use AI to analyze email priority
    Returns: 'urgent', 'important', or 'normal'
    
    Note: the newest OpenAI model is "gpt-5" which was released August 7, 2025.
    do not change this unless explicitly requested by the user
    """
    if not openai_client:
        return 'normal'
    
    try:
        prompt = f"""Analyze this email and categorize its priority level.

Subject: {subject}
From: {sender}
Preview: {snippet}

Categorize as one of:
- urgent: Requires immediate action (deadlines, urgent requests, time-sensitive)
- important: Significant but not time-critical (project updates, important decisions)
- normal: Regular communication (newsletters, routine updates, general info)

Respond with JSON in this exact format: {{"priority": "urgent|important|normal", "reason": "brief explanation"}}"""

        response = openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an email priority assistant. Analyze emails and categorize them accurately."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=200
        )
        
        result = json.loads(response.choices[0].message.content)
        priority = result.get('priority', 'normal').lower()
        
        if priority not in ['urgent', 'important', 'normal']:
            priority = 'normal'
        
        return priority
    except Exception as e:
        print(f"Error analyzing email priority: {e}")
        return 'normal'

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

@app.route("/gmail-authorize")
@login_required
def gmail_authorize():
    """Start OAuth flow for Gmail"""
    user = current_user()
    
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        flash("Gmail integration is not configured. Please contact administrator.", "danger")
        return redirect(url_for('email'))
    
    redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')
    
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
    redirect_uri = url_for('oauth2callback', _external=True, _scheme='https')
    
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
    
    authorization_response = request.url.replace('http://', 'https://')
    
    try:
        flow.fetch_token(authorization_response=authorization_response)
        
        credentials = flow.credentials
        save_user_gmail_credentials(user['id'], credentials)
        
        flash("Gmail connected successfully!", "success")
        return redirect(url_for('email'))
    except Exception as e:
        flash(f"Failed to connect Gmail: {str(e)}", "danger")
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
            
            if openai_client and OPENAI_API_KEY:
                email_info['priority'] = analyze_email_priority(
                    email_info['subject'],
                    email_info['sender'],
                    email_info['snippet']
                )
            else:
                email_info['priority'] = 'normal'
            
            emails.append(email_info)
        
        return render_template("email.html", user=user, emails=emails, connected=True)
    
    except Exception as e:
        print(f"Error fetching emails: {str(e)}")
        flash(f"Error fetching emails: {str(e)}", "danger")
        return render_template("email.html", user=user, emails=[], connected=False)

@app.route("/calendar")
@login_required
def calendar():
    user = current_user()
    calendar_service = get_calendar_service()
    
    if not calendar_service:
        return render_template("calendar.html", user=user, events=[], connected=False)
    
    try:
        now = datetime.now(timezone.utc).isoformat()
        events_result = calendar_service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=20,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            try:
                if 'T' in start:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    start_formatted = start_dt.strftime('%b %d, %Y at %I:%M %p')
                else:
                    start_dt = datetime.fromisoformat(start)
                    start_formatted = start_dt.strftime('%b %d, %Y')
            except:
                start_formatted = start
            
            formatted_events.append({
                'id': event['id'],
                'summary': event.get('summary', 'No Title'),
                'start': start_formatted,
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'htmlLink': event.get('htmlLink', '')
            })
        
        return render_template("calendar.html", user=user, events=formatted_events, connected=True)
    
    except Exception as e:
        print(f"Error fetching calendar events: {str(e)}")
        flash(f"Error fetching calendar events: {str(e)}", "danger")
        return render_template("calendar.html", user=user, events=[], connected=False)

@app.route("/reports")
@login_required
def reports():
    return render_template("feature.html", title="Reports", subtitle="Weekly PDF/Word reports will appear here…")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
