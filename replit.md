# SmartOffice AI

## Overview
SmartOffice AI is a Flask-based web application that serves as an intelligent admin assistant. The application provides user authentication and is designed to integrate with Gmail, Google Calendar, and generate smart weekly reports.

**Current Status**: Development environment configured and running successfully on Replit.

## Recent Changes (October 7, 2025)
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
│   │   └── style.css      # Custom styles with logo design
│   └── images/
│       └── smartoffice-logo.svg  # Downloadable logo file
├── templates/
│   ├── base.html          # Base template with navbar and logo
│   ├── index.html         # Dashboard
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── email.html         # Gmail inbox display
│   └── feature.html       # Feature placeholder pages
└── .gitignore            # Python gitignore
```

### Key Features
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

5. **Planned Features**
   - AI-powered email priority categorization
   - AI email reply suggestions
   - Automated PDF/Word report generation
   - Bilingual interface support (English/Arabic)

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
