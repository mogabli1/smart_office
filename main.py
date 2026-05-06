from flask import Flask, request, redirect, render_template, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder='static', template_folder='.')

# Configuration - These should be set as Environment Variables in Render
GMAIL_USER = os.environ.get('GMAIL_USER')  # Your Gmail address
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')  # Your Gmail App Password
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', GMAIL_USER) # Where you want to receive emails

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index_redirect():
    return render_template('index.html')

@app.route('/contact.html')
def contact_page():
    return render_template('contact.html')

@app.route('/privacy.html')
def privacy_page():
    return render_template('privacy.html')

@app.route('/terms.html')
def terms_page():
    return render_template('terms.html')

@app.route('/success.html')
def success_page():
    return render_template('success.html')

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    interest = request.form.get('interest')
    message_content = request.form.get('message')

    print(f"DEBUG: Received submission from {name} ({email})")

    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("DEBUG: ERROR - Gmail credentials missing!")
        return "Server Error: Gmail credentials not configured in Render environment variables.", 500

    # Create Email
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"New Project Request: {interest} from {name}"

    body = f"""
    New message from your website:
    
    Name: {name}
    Business Email: {email}
    Interest: {interest}
    
    Message:
    {message_content}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("DEBUG: Connecting to smtp.gmail.com:465 (SSL)...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
        
        print(f"DEBUG: Attempting login for {GMAIL_USER}...")
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        
        print("DEBUG: Sending email...")
        text = msg.as_string()
        server.sendmail(GMAIL_USER, RECEIVER_EMAIL, text)
        
        print("DEBUG: Closing connection...")
        server.quit()
        
        print("DEBUG: SUCCESS! Redirecting to success page.")
        return redirect('/success.html')
    except Exception as e:
        print(f"DEBUG: EXCEPTION caught: {e}")
        return f"Failed to send message. Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
