# 🎬 SmartOffice AI - Google OAuth Verification Demo Video Script

**Target Duration:** 6-8 minutes  
**Recording Tool:** Loom, OBS Studio, or QuickTime  
**Upload To:** YouTube (Unlisted) or Google Drive

---

## 📋 Pre-Recording Checklist

- [ ] Clear browser cache and cookies
- [ ] Use incognito/private window for clean OAuth flow
- [ ] Test Gmail account ready (with emails and calendar events)
- [ ] Stable internet connection
- [ ] Close unnecessary tabs/apps
- [ ] Enable microphone for narration
- [ ] Practice run-through once

---

## 🎥 Video Script with Timing

### **Scene 1: Introduction (0:00 - 0:45)**

**What to Show:**
- Open browser to: https://www.smartoffice-ai.com
- Show landing page with logo and features

**What to Say:**
> "Hello, I'm demonstrating SmartOffice AI, an intelligent admin assistant for small and medium enterprises. SmartOffice AI uses artificial intelligence to help busy professionals manage their emails, calendars, and generate automated reports. The application integrates with Gmail and Google Calendar through OAuth 2.0, ensuring complete data privacy - each user connects their own accounts."

**Key Points to Highlight:**
- Show the landing page
- Scroll through features section
- Mention bilingual support (English/Arabic)

---

### **Scene 2: User Authentication (0:45 - 1:30)**

**What to Show:**
- Click "Sign Up" button
- Fill registration form:
  - Email: demo@example.com
  - Name: Demo User
  - Password: (hidden)
- Click "Register"
- Show successful registration
- Login with credentials

**What to Say:**
> "First, users create an account with their email and password. The application uses secure password hashing with Werkzeug. After registration, users can log in to access the dashboard."

**Key Points:**
- Show registration form fields clearly
- Demonstrate successful login
- Show dashboard after login

---

### **Scene 3: Gmail OAuth Integration (1:30 - 3:30)**

**What to Show:**
1. Click "Email" from dashboard navigation
2. Show "Connect Gmail" button
3. Click "Connect Gmail" - OAuth flow begins
4. **CRITICAL: Show Google OAuth consent screen**
   - Project name: SmartOffice AI
   - Requested scope: Gmail readonly
   - Show permission details
5. Click "Allow" / "Continue"
6. Redirect back to app
7. Show inbox with emails loaded

**What to Say:**
> "To access Gmail, users click the Email section and authorize Gmail access. This starts Google's OAuth 2.0 flow. The application requests only 'gmail.readonly' scope - this means read-only access to emails. Users can see exactly what permissions are being requested. After granting permission, the application securely stores OAuth tokens in the database, unique to each user. Here we see the user's inbox successfully loaded."

**Key Points to Emphasize:**
- ✅ Show the FULL OAuth consent screen (Google's official screen)
- ✅ Point out the "gmail.readonly" scope
- ✅ Explain read-only access (no sending, no deleting)
- ✅ Show successful email loading
- ✅ Mention token storage per user

**Visual Checklist:**
- [ ] OAuth consent screen clearly visible
- [ ] Scope permissions shown
- [ ] Successful redirect to app
- [ ] Emails displayed in inbox

---

### **Scene 4: AI Email Features (3:30 - 5:30)**

**What to Show:**
1. **AI Priority Categorization**
   - Scroll through inbox
   - Point out priority badges (Urgent/Important/Normal)
   - Explain GPT-5 AI categorization

2. **AI Reply Suggestions**
   - Click on an email to open details
   - Show 3 AI-generated reply options
   - Highlight different tones: Professional, Friendly, Brief
   - Click "Copy" button on one suggestion
   - Show copied confirmation

**What to Say:**
> "SmartOffice AI uses GPT-5 to automatically categorize emails by priority. Each email gets a badge - Urgent for time-sensitive items, Important for key business matters, and Normal for routine emails. This helps users focus on what matters most.

> Additionally, the AI generates smart reply suggestions. For each email, users get three response options in different tones: Professional for formal communication, Friendly for casual exchanges, and Brief for quick responses. Users can copy any suggestion with one click and paste it into their email client."

**Key Points:**
- Show priority badges clearly
- Demonstrate all 3 reply tones
- Show copy functionality working

---

### **Scene 5: Google Calendar Integration (5:30 - 6:30)**

**What to Show:**
1. Click "Calendar" from dashboard
2. Show "Connect Google Calendar" button (if first time)
3. **Show OAuth consent screen for Calendar**
   - Scope: calendar.readonly
4. Click "Allow"
5. Show upcoming calendar events displayed
   - Event titles
   - Date/time
   - Location (if any)
   - Descriptions

**What to Say:**
> "Calendar integration works similarly. The application requests 'calendar.readonly' scope for read-only access to the user's Google Calendar. After authorization, upcoming events are displayed with full details - titles, times, locations, and descriptions. Users can click to view events directly in Google Calendar."

**Key Points:**
- Show calendar OAuth consent
- Display multiple calendar events
- Show event details clearly

---

### **Scene 6: Automated Report Generation (6:30 - 7:30)**

**What to Show:**
1. Click "Reports" from dashboard
2. Show report generation options
3. Click "Generate PDF Report"
   - Show loading/processing
   - PDF download starts
   - Open PDF to show contents:
     - Header with SmartOffice AI branding
     - Email summary section
     - Calendar events section
4. Click "Generate Word Report"
   - Word file downloads
   - Open Word file briefly to show formatted content

**What to Say:**
> "The Reports feature automatically generates professional documents combining email summaries and calendar data. Users can export to PDF or Word format with one click. The reports include email statistics, priority breakdowns, and upcoming calendar events - perfect for weekly summaries or client updates."

**Key Points:**
- Show both PDF and Word generation
- Open at least one report to show contents
- Highlight professional formatting

---

### **Scene 7: Bilingual Support (7:30 - 8:00)**

**What to Show:**
1. Click language switcher in navigation
2. Select "العربية" (Arabic)
3. Show interface switch to Arabic
4. Show RTL (right-to-left) layout
5. Navigate through features in Arabic
6. Switch back to English

**What to Say:**
> "SmartOffice AI supports both English and Arabic with full right-to-left layout for Arabic users. The entire interface adapts instantly, making it accessible to a broader audience in the Middle East and globally."

**Key Points:**
- Show smooth language transition
- Demonstrate RTL layout
- Show navigation still works perfectly

---

### **Scene 8: Data Privacy & Security (8:00 - 8:30)**

**What to Show:**
- Navigate to Privacy Policy (footer link)
- Scroll through key sections
- Return to dashboard
- Show user's connected accounts

**What to Say:**
> "Regarding data privacy: SmartOffice AI implements OAuth 2.0 best practices. Each user connects their own Gmail and Google Calendar accounts - there is no shared data between users. OAuth tokens are encrypted and stored securely in the database. The application never accesses data without explicit user consent, and users can revoke access at any time through their Google Account settings."

**Key Points:**
- Emphasize per-user OAuth tokens
- No shared data architecture
- User control over permissions
- Compliance with Google's policies

---

### **Scene 9: Conclusion (8:30 - 9:00)**

**What to Show:**
- Return to landing page
- Show footer with Privacy Policy and Terms links

**What to Say:**
> "In summary, SmartOffice AI provides AI-powered email management, smart calendar integration, and automated reporting while maintaining strict data privacy. The application uses OAuth 2.0 for secure, user-controlled access to Gmail and Google Calendar. Each user's data remains private and isolated. Thank you for reviewing this demonstration."

**Final Points:**
- Recap key features
- Emphasize OAuth security
- Thank reviewers

---

## 🎬 Recording Tips

### **Before Recording:**
1. **Test the flow**: Run through everything once before recording
2. **Prepare test data**: Have emails and calendar events ready
3. **Clean environment**: Close unnecessary tabs, hide personal info
4. **Good audio**: Use a decent microphone, minimize background noise

### **During Recording:**
1. **Speak clearly**: Narrate each action as you perform it
2. **Slow down**: Give viewers time to see what's happening
3. **Highlight important parts**: Use cursor movement to draw attention
4. **Show OAuth screens fully**: This is what Google wants to see most

### **After Recording:**
1. **Review the video**: Watch it once to check quality
2. **Verify OAuth screens are visible**: This is critical for approval
3. **Check audio levels**: Make sure narration is clear
4. **Upload as Unlisted**: YouTube unlisted or Google Drive with link sharing

---

## ✅ Google Review Checklist

Make sure your video shows:

- [x] **OAuth Consent Screens** - Both Gmail and Calendar authorization screens fully visible
- [x] **Scope Details** - gmail.readonly and calendar.readonly scopes clearly shown
- [x] **User Flow** - Complete flow from login to feature usage
- [x] **App Functionality** - All key features demonstrated
- [x] **Data Privacy** - Explanation of per-user OAuth and data isolation
- [x] **Professional Quality** - Clear audio, smooth demonstration, no errors

---

## 📤 Upload Instructions

### **Option 1: YouTube (Recommended)**
1. Upload video to YouTube
2. Set visibility to "Unlisted"
3. Copy the link (looks like: https://youtu.be/xxxxx)
4. Share in email to Google

### **Option 2: Google Drive**
1. Upload video to Google Drive
2. Right-click → Share → Anyone with link can view
3. Copy link
4. Share in email to Google

### **Option 3: Loom**
1. Record directly in Loom
2. Copy share link
3. Share in email to Google

---

## 🚨 Common Mistakes to Avoid

❌ **Don't:**
- Skip showing the OAuth consent screen (most important!)
- Use fake/mock data that looks unrealistic
- Show errors or failed flows
- Have poor audio quality
- Rush through important parts
- Show sensitive personal information

✅ **Do:**
- Show complete OAuth flow with Google's consent screens
- Use realistic test data
- Demonstrate smooth, error-free operation
- Narrate clearly what's happening
- Take time to show each feature
- Emphasize security and privacy

---

## 📧 After Video is Ready

Send this exact information to Google:

**Subject:** Re: OAuth Verification - Demo Video & Redirect URI Fixed

**Body:**
```
Hi Third Party Data Safety Team,

I have addressed both issues:

1. ✅ Demo Video: [INSERT_YOUR_VIDEO_LINK_HERE]

The video demonstrates:
- Complete OAuth 2.0 consent flow for Gmail (gmail.readonly scope)
- Complete OAuth 2.0 consent flow for Google Calendar (calendar.readonly scope)  
- AI-powered email priority categorization using GPT-5
- AI email reply suggestions in multiple tones
- Automated PDF/Word report generation
- Bilingual interface (English/Arabic)
- Data privacy: Each user connects their own accounts with isolated OAuth tokens

2. ✅ Redirect URI Fixed: All authorized redirect URIs have been updated in Google Cloud Console for project smartofficeai-474419 to match our production domain (www.smartoffice-ai.com) and deployment URLs.

Production URIs:
- https://www.smartoffice-ai.com/oauth2callback
- https://www.smartoffice-ai.com/calendar_oauth2callback

Please let me know if you need any additional information.

Thank you,
[Your Name]
```

---

## 🎯 Success Criteria

Your video will be approved if it clearly shows:

1. ✅ Real OAuth consent screens from Google
2. ✅ Accurate scope requests (readonly only)
3. ✅ Working integration with Gmail and Calendar
4. ✅ Legitimate use case (business productivity)
5. ✅ Data privacy and security measures
6. ✅ Professional, functional application

---

**Good luck with your recording! Follow this script and Google should approve your OAuth verification.** 🚀
