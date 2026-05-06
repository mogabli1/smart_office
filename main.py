from flask import Flask, request, redirect, render_template, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static', template_folder='.')

# Configuration
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', 'info@smartoffice-ai.com')

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

    if not RESEND_API_KEY:
        print("DEBUG: ERROR - RESEND_API_KEY missing!")
        return "Server Error: Email service not configured.", 500

    try:
        print("DEBUG: Sending via Resend API...")
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": "SmartOffice AI <onboarding@resend.dev>",
                "to": RECEIVER_EMAIL,
                "subject": f"New Request: {interest} from {name}",
                "html": f"""
                <h3>New message from your website:</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Business Email:</strong> {email}</p>
                <p><strong>Interest:</strong> {interest}</p>
                <p><strong>Message:</strong></p>
                <p>{message_content}</p>
                """
            }
        )
        
        if response.status_code in [200, 201]:
            print("DEBUG: SUCCESS! Resend accepted the email.")
            return redirect('/success.html')
        else:
            print(f"DEBUG: Resend API Error: {response.status_code} - {response.text}")
            return f"Failed to send message. Service Error: {response.text}", 500
            
    except Exception as e:
        print(f"DEBUG: EXCEPTION caught: {e}")
        return f"Failed to send message. Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
