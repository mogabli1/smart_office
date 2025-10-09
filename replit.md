# SmartOffice AI

## Overview
SmartOffice AI is a Flask-based web application that serves as an intelligent admin assistant. The application provides user authentication and is designed to integrate with Gmail, Google Calendar, and generate smart weekly reports.

**Current Status**: Development environment configured and running successfully on Replit.

## Recent Changes (October 9, 2025)
- **✅ DEPLOYED TO PRODUCTION** - Live at www.smartoffice-ai.com and smartoffice-mogabli1.replit.app
- **✅ DOMAIN VERIFIED & SSL CERTIFICATE ISSUED** - Custom domain fully functional with valid HTTPS
- **✅ GOOGLE ANALYTICS ACTIVE** - GA4 tracking installed (Measurement ID: G-4RFV9LCB1N)
- **✅ GOOGLE SEARCH CONSOLE VERIFIED** - Domain verified and sitemap submitted successfully
- **DNS Configuration Fixed** - Removed conflicting CAA records that were blocking SSL certificate generation
- **Sitemap Created** - XML sitemap at /sitemap.xml with all public pages for SEO
- **Email Addresses Fixed** - Corrected all contact emails to info@smartoffice-ai.com across Privacy, Terms, and Contact pages
- **Test Gmail Integration Route** - Added /test-gmail for alternative OAuth testing (requires client_secret JSON file)

## Previous Changes (October 8, 2025)
- **Enhanced Landing Pages** - Redesigned with professional navigation header, smaller pricing card, 6 feature cards
- Added sticky navigation bar with logo, language switcher, Login, and Sign Up buttons
- **Testing Phase Notification System** - Added prominent alert and modal on pricing page
- Implemented session-aware modal: redirects to dashboard if logged in, registration if not
- **Email Forwarding Setup** - Contact form submissions now forward to mogabli12@gmail.com
- Integrated Replit Mail API for professional HTML email formatting with customer details
- Implemented Bilingual Public Landing Pages - Beautiful English and Arabic landing pages
- Added auto-refresh functionality with dual-method approach (window.opener + localStorage fallback)
- Created Privacy Policy and Terms of Service pages with footer links
- Updated Terms to flexible pricing (allows changes with 30-day notice)

## Previous Changes (October 7, 2025)
- Migrated from GitHub import to Replit environment
- Fixed deprecated `@app.before_first_request` decorator (Flask 3.0 compatibility)
- Configured application to run on port 5000 for Replit hosting
- Added Gunicorn for production deployment
- Created Python .gitignore file
- Set up deployment configuration with autoscale
- Created professional gradient logo (purple "SO" icon)
- **Implemented Manual Gmail OAuth Integration** - full inbox access with gmail.readonly scope
- Added OAuth flow with Google Cloud credentials for Gmail API access
- Created database table to store OAuth tokens per user
- Added Gmail authorization and callback routes
- **Fixed OAuth https redirect URI handling** - forced https scheme for proper Google OAuth
- **Improved email inbox UI** - modern card design with hover effects
- **Fixed critical refresh token bug** - preserves refresh tokens on re-authorization
- Cleaned up debug code and logging
- **Implemented Google Calendar Integration** - using Replit connector for seamless authentication
- Added calendar route to display upcoming events with modern UI
- Created helper functions to fetch access tokens from Replit connector API
- **✅ ALL 5 CORE FEATURES COMPLETED:**
  - AI Email Priority Categorization (GPT-5 powered - ready when credits added)
  - AI Email Reply Suggestions (3 tones with copy functionality)
  - PDF/Word Report Generation (ReportLab + python-docx)
  - Bilingual Interface (English/Arabic with RTL support and language switcher)

## Project Architecture

### Technology Stack
- **Backend Framework**: Flask 3.0.0
- **Database**: SQLite3 (local file-based database)
- **Authentication**: Werkzeug password hashing
- **Production Server**: Gunicorn 21.2.0
- **Frontend**: Bootstrap 5.3.2 with custom CSS (Poppins font)
- **Gmail Integration**: Google API Python Client with Replit Connector
- **Logo**: Custom gradient SVG logo (purple "SO" branding)

### File Structure
```
.
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── smartoffice.db         # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   ├── style.css         # Dashboard styles with logo design
│   │   ├── landing.css       # English landing page styles
│   │   └── landing-ar.css    # Arabic landing page styles
│   └── images/
│       └── smartoffice-logo.svg  # Downloadable logo file
├── templates/
│   ├── landing.html       # Public landing page (English)
│   ├── landing_ar.html    # Public landing page (Arabic)
│   ├── base.html          # Base template with navbar and logo
│   ├── index.html         # Dashboard (protected)
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── email.html         # Gmail inbox display
│   ├── calendar.html      # Google Calendar display
│   ├── reports.html       # Report generation page
│   ├── pricing.html       # Stripe subscription pricing
│   ├── success.html       # Payment success page
│   ├── privacy.html       # Privacy Policy
│   └── terms.html         # Terms of Service
└── .gitignore            # Python gitignore
```

### Key Features
0. **Public Landing Pages** (NEW!)
   - Beautiful bilingual landing pages (English/Arabic)
   - Smooth fade-in animations
   - Clean gradient backgrounds
   - Feature showcase cards with hover effects
   - Language switcher with flag icons
   - Direct CTAs to Demo and Early Access signup
   - Fully responsive design
   - No login required to view

1. **User Authentication**
   - Registration with email, name, and password
   - Secure login with password hashing
   - Session management
   - Protected routes with `@login_required` decorator

2. **Dashboard & Navigation**
   - User dashboard with welcome message
   - Navigation to Email, Calendar, and Reports features
   - Flash messaging for user feedback

3. **Gmail Integration** (ACTIVE)
   - Manual OAuth 2.0 integration with Google Cloud credentials
   - Full gmail.readonly scope for complete inbox access
   - Per-user token storage in database
   - OAuth authorization flow with callback handling
   - Displays user's inbox (last 15 emails)
   - Shows subject, sender, date, and snippet
   - "Connect Gmail" button for easy authorization

4. **Google Calendar Integration** (ACTIVE)
   - Integrated via Replit connector (project-level OAuth)
   - Displays up to 20 upcoming calendar events
   - Shows event title, date/time, location, and description
   - Links to view events in Google Calendar
   - Modern card-based UI with hover effects
   - Automatic token refresh handled by Replit

5. **AI Features** (✅ COMPLETED)
   - **Email Priority Categorization**: GPT-5 analyzes each email and assigns priority badges (Urgent/Important/Normal)
   - **Email Reply Suggestions**: Generates 3 reply options in different tones (Professional/Friendly/Brief) with one-click copy
   - Graceful degradation when OPENAI_API_KEY is unavailable
   - Smart error handling for quota limits

6. **Report Generation** (✅ COMPLETED)
   - Automated PDF report generation using ReportLab
   - Automated Word document generation using python-docx
   - Includes email summary and calendar events
   - Proper HTML text escaping for special characters
   - Professional formatting with headers and tables

7. **Bilingual Interface** (✅ COMPLETED)
   - Full English/Arabic language support
   - Language switcher dropdown in navbar
   - RTL (right-to-left) layout support for Arabic
   - Cairo font for Arabic text, Poppins for English
   - 30+ translated strings covering key UI elements
   - Session-based language persistence

### Database Schema
**users table**:
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `email` (TEXT UNIQUE NOT NULL)
- `name` (TEXT NOT NULL)
- `password_hash` (TEXT NOT NULL)
- `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask session secret (defaults to "dev-secret-change-me" in development)
- `DB_PATH`: Database file path (defaults to "smartoffice.db")
- `PORT`: Server port (defaults to 5000)

### Development Setup
- Server runs on `0.0.0.0:5000` with debug mode enabled
- Development server: `python main.py`
- Database is automatically initialized on first run

### Deployment Setup
- Deployment target: **autoscale** (stateless web application)
- Production server: Gunicorn with 2 workers on port 5000
- Command: `gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 main:app`

## Development Notes

### Flask 3.0 Migration
The original code used the deprecated `@app.before_first_request` decorator, which was removed in Flask 3.0. This has been replaced with `app.app_context()` to initialize the database:

```python
with app.app_context():
    init_db()
```

### Security Considerations
- Change `SECRET_KEY` in production environment
- Passwords are hashed using Werkzeug's `generate_password_hash`
- Email addresses are normalized to lowercase for consistency
- SQLite database should be backed up regularly

## Next Steps for Development
1. Implement Gmail API integration for email management
2. Implement Google Calendar API integration
3. Build report generation functionality (PDF/Word)
4. Add environment-based configuration (production vs development)
5. Consider migrating to PostgreSQL for production scalability
6. Add password strength validation
7. Implement password reset functionality
8. Add email verification for new accounts
