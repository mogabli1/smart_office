# 🧪 GOOGLE OAUTH TESTING INSTRUCTIONS

**For:** Google Third Party Data Safety Team  
**Project:** SmartOffice AI (smartofficeai-474419)  
**Issue:** Free trial enabled for OAuth testing  
**Date:** October 13, 2025

---

## ✅ FREE TRIAL NOW ENABLED FOR TESTING

In response to your request, we have **enabled a 14-day free trial** for all new user registrations. Google's testing team can now access and test the OAuth consent workflow without requiring a paid subscription.

---

## 📋 HOW TO TEST OAUTH CONSENT WORKFLOW

### **Step 1: Create Test Account (No Payment Required)**

1. **Go to:** https://www.smartoffice-ai.com
2. **Click:** "Sign Up" button in the top navigation
3. **Register with test credentials:**
   - Name: (any name)
   - Email: (your Google test email)
   - Password: (any password)
4. **Click:** "Sign Up"
5. **Result:** Account created with **automatic 14-day free trial** - NO payment or subscription required

**Success message will show:** 
> "🎉 Account created! You have 14 days of free trial access. Please log in."

### **Step 2: Log In**

1. **Click:** "Login" button
2. **Enter:** Email and password from Step 1
3. **Click:** "Login"
4. **Result:** Dashboard loads with access to all features

### **Step 3: Test Gmail OAuth Consent Flow**

1. **From Dashboard, click:** "Email" in navigation menu (or "Connect Gmail" button)
2. **OAuth consent screen appears** with:
   - App name: SmartOffice AI
   - Requested scope: "See and download your email messages and settings"
   - Scope: `https://www.googleapis.com/auth/gmail.readonly`
3. **Click the blue link:** "See the 1 service SmartOffice AI wants to access"
4. **Permissions expand** showing:
   - ✓ View email messages and settings
   - ✗ NO permissions to send, delete, or modify emails (read-only)
5. **Click:** "Continue" to authorize
6. **Result:** Redirects to app showing Gmail inbox with emails loaded

### **Step 4: Test Google Calendar OAuth Consent Flow**

1. **From Dashboard, click:** "Calendar" in navigation menu (or "Connect Calendar" button)
2. **OAuth consent screen appears** with:
   - App name: SmartOffice AI
   - Requested scope: "See and download any calendar you can access using your Google Calendar"
   - Scope: `https://www.googleapis.com/auth/calendar.readonly`
3. **Click the blue link** to expand permissions
4. **Permissions expand** showing:
   - ✓ See personal and shared calendars
   - ✓ See and download calendar events
   - ✗ NO permissions to create, edit, or delete events (read-only)
5. **Click:** "Continue" to authorize
6. **Result:** Redirects to app showing Calendar events loaded

### **Step 5: Test Feature Usage (Optional)**

After authorizing both OAuth scopes, you can test:

- **Email Priority Categorization:** View emails with AI-generated priority badges (Urgent/Important/Normal)
- **Smart Reply Suggestions:** Click on any email to see AI-generated reply suggestions
- **Calendar Integration:** View upcoming calendar events
- **Report Generation:** Click "Reports" to generate PDF/Word reports combining email and calendar data

---

## 🔑 KEY TESTING POINTS TO VERIFY

### **OAuth Consent Screens:**
✅ Both Gmail and Calendar consent screens display correctly  
✅ Scopes shown match verification request (gmail.readonly + calendar.readonly)  
✅ "See service details" links work and show expanded permissions  
✅ Read-only nature is clear (no create/edit/delete permissions)  
✅ Continue button authorizes successfully  

### **Data Usage:**
✅ Gmail data used ONLY for email categorization and reply suggestions displayed to user  
✅ Calendar data used ONLY for event display and report generation  
✅ No data used for AI training, marketing, or third-party sharing  
✅ Users can revoke access anytime via Google Account settings  

### **Free Trial Access:**
✅ New registrations automatically get 14-day trial  
✅ No payment required to test OAuth flow  
✅ All features accessible during trial period  

---

## 🎬 DEMO VIDEO REFERENCE

Complete OAuth demonstration video: **https://youtu.be/Rjp_iSLuFDI**

The video shows:
- Gmail OAuth consent flow with expanded permissions
- Calendar OAuth consent flow with expanded permissions  
- Email and calendar data loading after authorization
- Read-only scope explanation
- Data privacy and security features

---

## 📞 TEST ACCOUNT ASSISTANCE

If the testing team encounters any issues:

1. **Trial period confirmation:** Check for success message after registration showing "14 days of free trial access"
2. **OAuth errors:** All redirect URIs are configured correctly - no redirect_uri_mismatch errors
3. **Scope verification:** Only 2 scopes requested (gmail.readonly + calendar.readonly)

**Support contact:** info@smartoffice-ai.com

---

## ✅ COMPLIANCE SUMMARY

**Privacy Policy:** Updated October 13, 2025 at https://www.smartoffice-ai.com/privacy
- Removed prohibited use of data for AI model training
- Added explicit Limited Use compliance section
- Listed prohibited uses (marketing, analytics, training, third-party sharing)

**OAuth Scopes:** Configured in Google Cloud Console
- gmail.readonly (read-only email access)
- calendar.readonly (read-only calendar access)
- No extra scopes (removed: openid, userinfo.email, userinfo.profile)

**Free Trial:** ENABLED for testing
- 14-day free trial for all new registrations
- No payment or subscription required
- Full feature access during trial

---

## 🚀 READY FOR TESTING

The OAuth consent workflow is now fully accessible to Google's testing team without any payment barriers.

Please proceed with testing and let us know if you need any additional information or test accounts.

Thank you for your thorough review process.

---

**Submitted by:** Sami Mohamed  
**Website:** https://www.smartoffice-ai.com  
**Email:** info@smartoffice-ai.com  
**Project ID:** smartofficeai-474419
