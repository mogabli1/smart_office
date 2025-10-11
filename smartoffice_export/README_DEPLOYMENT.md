# SmartOffice AI - Complete Deployment Package

## 📦 What's Included

This package contains everything you need to host SmartOffice AI on any platform:

```
smartoffice_export/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/              # All HTML templates
├── static/                 # CSS, images, and assets
├── .gitignore             # Git ignore file
├── Procfile               # For Heroku deployment
├── runtime.txt            # Python version specification
└── README_DEPLOYMENT.md   # This file
```

## 🚀 Deployment Options

### Option 1: Heroku (Easiest)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Login to Heroku**:
   ```bash
   heroku login
   ```
3. **Create a new app**:
   ```bash
   heroku create smartoffice-ai
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set STRIPE_SECRET_KEY="your-stripe-key"
   heroku config:set GOOGLE_CLIENT_ID="your-google-client-id"
   heroku config:set GOOGLE_CLIENT_SECRET="your-google-secret"
   heroku config:set OPENAI_API_KEY="your-openai-key"
   ```
5. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```
6. **Open your app**:
   ```bash
   heroku open
   ```

### Option 2: DigitalOcean App Platform

1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect your GitHub repo or upload these files
4. DigitalOcean will auto-detect Flask app
5. Add environment variables in Settings
6. Deploy!

**Pricing**: $5-12/month

### Option 3: AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI
2. Initialize:
   ```bash
   eb init -p python-3.11 smartoffice-ai
   ```
3. Create environment:
   ```bash
   eb create smartoffice-production
   ```
4. Set environment variables in AWS Console
5. Deploy:
   ```bash
   eb deploy
   ```

### Option 4: Railway.app (Modern Alternative)

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Connect repo or upload files
4. Add environment variables
5. Deploy automatically!

**Pricing**: $5/month

### Option 5: VPS (Ubuntu Server)

For full control, deploy on any VPS (DigitalOcean, Linode, AWS EC2):

1. **SSH into your server**:
   ```bash
   ssh root@your-server-ip
   ```

2. **Install Python and dependencies**:
   ```bash
   apt update
   apt install python3-pip python3-venv nginx -y
   ```

3. **Clone your files** (or upload via SCP/SFTP)

4. **Create virtual environment**:
   ```bash
   cd /var/www/smartoffice
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

6. **Create systemd service** (`/etc/systemd/system/smartoffice.service`):
   ```ini
   [Unit]
   Description=SmartOffice AI
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/smartoffice
   Environment="PATH=/var/www/smartoffice/venv/bin"
   ExecStart=/var/www/smartoffice/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 4 main:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx** (`/etc/nginx/sites-available/smartoffice`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

8. **Enable and start**:
   ```bash
   systemctl enable smartoffice
   systemctl start smartoffice
   ln -s /etc/nginx/sites-available/smartoffice /etc/nginx/sites-enabled/
   systemctl restart nginx
   ```

9. **Setup SSL with Let's Encrypt**:
   ```bash
   apt install certbot python3-certbot-nginx -y
   certbot --nginx -d your-domain.com
   ```

## 🔐 Required Environment Variables

You must set these environment variables on your hosting platform:

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `SECRET_KEY` | Flask session secret | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `STRIPE_SECRET_KEY` | Stripe payment key | https://dashboard.stripe.com/apikeys |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | https://console.cloud.google.com |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | https://console.cloud.google.com |
| `OPENAI_API_KEY` | OpenAI API key | https://platform.openai.com/api-keys |

## 📊 Database

The app uses SQLite by default (file-based database). For production, consider:

### Upgrade to PostgreSQL (Recommended for production):

1. **Update requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```

2. **Set DATABASE_URL**:
   ```bash
   export DATABASE_URL="postgresql://user:password@host:5432/dbname"
   ```

3. **Modify main.py** (replace SQLite connection with PostgreSQL)

Most hosting platforms offer managed PostgreSQL databases.

## ⚙️ Configuration Flags

In `main.py`, you can control features:

```python
PRICING_ENABLED = True          # Enable/disable pricing page
FREE_TRIAL_ENABLED = False      # Enable 14-day free trial
FREE_TRIAL_DAYS = 14           # Trial duration
```

## 🌐 Custom Domain Setup

After deploying, point your domain:

1. **Add DNS records**:
   - Type: `A` Record
   - Name: `@` or `www`
   - Value: Your server IP or provided by platform

2. **Update Stripe redirect URLs** in dashboard

3. **Update Google OAuth redirect URIs** in console

## 📝 Post-Deployment Checklist

- [ ] Set all environment variables
- [ ] Test user registration and login
- [ ] Test Gmail OAuth connection
- [ ] Test Google Calendar integration
- [ ] Test Stripe payment flow (use test mode first!)
- [ ] Test PDF/Word report generation
- [ ] Test email sending (contact form)
- [ ] Verify SSL certificate is active
- [ ] Check mobile responsiveness
- [ ] Submit sitemap to Google Search Console
- [ ] Set up monitoring/logging

## 🔧 Troubleshooting

### Common Issues:

**"Module not found" errors**:
- Run: `pip install -r requirements.txt`

**Database errors**:
- Ensure `smartoffice.db` has write permissions
- Or migrate to PostgreSQL for production

**OAuth redirect errors**:
- Update redirect URIs in Google Cloud Console to match your domain

**Stripe webhook issues**:
- Set up Stripe webhooks in dashboard pointing to your domain

## 📦 Dependencies

All dependencies are in `requirements.txt`:
- Flask 3.0.0 (web framework)
- Gunicorn 21.2.0 (production server)
- Stripe (payments)
- Google API Client (Gmail, Calendar)
- OpenAI (AI features)
- ReportLab (PDF generation)
- python-docx (Word generation)

## 💰 Estimated Hosting Costs

| Platform | Cost/Month | Best For |
|----------|------------|----------|
| Heroku | $7-25 | Easy deployment |
| Railway | $5-10 | Modern, simple |
| DigitalOcean | $6-12 | Good balance |
| AWS | $5-20 | Scalability |
| VPS | $5-10 | Full control |

## 🆘 Support

For deployment issues:
- Check platform documentation
- Verify all environment variables are set
- Check application logs for errors
- Test locally first: `python main.py`

## 📞 Need Help?

Contact: info@smartoffice-ai.com

---

**Good luck with your deployment! 🚀**

Your app is production-ready and includes:
✅ User authentication
✅ Stripe subscription payments ($19.99/month)
✅ Gmail integration with OAuth
✅ Google Calendar integration
✅ AI-powered email features (GPT)
✅ PDF/Word report generation
✅ Bilingual interface (English/Arabic)
✅ Mobile-responsive design
✅ SEO optimized
✅ Google Analytics integrated
