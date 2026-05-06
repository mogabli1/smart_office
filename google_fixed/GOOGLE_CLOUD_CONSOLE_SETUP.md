# 🔧 Google Cloud Console OAuth Setup Guide

## Project Information
- **Project ID:** smartofficeai-474419
- **Project Number:** 596418050127
- **Application Name:** SmartOffice AI

---

## ✅ Required Redirect URIs

### **Production Domain (Primary)**
```
https://www.smartoffice-ai.com/oauth2callback
https://www.smartoffice-ai.com/calendar_oauth2callback
```

### **Replit Deployment (Secondary)**
```
https://smartoffice-mogabli1.replit.app/oauth2callback
https://smartoffice-mogabli1.replit.app/calendar_oauth2callback
```

### **Development Domain (Optional - for testing)**
```
https://96ee5be3-c82c-461f-815f-1879787c70fa-00-36haqnmfpcg7h.spock.replit.dev/oauth2callback
https://96ee5be3-c82c-461f-815f-1879787c70fa-00-36haqnmfpcg7h.spock.replit.dev/calendar_oauth2callback
```

---

## 📋 Step-by-Step Configuration

### **Step 1: Access Google Cloud Console**

1. Go to: https://console.cloud.google.com
2. Sign in with your Google account
3. Click on the project selector (top bar)
4. Select: **smartofficeai-474419**

✅ **Verification:** Check that "smartofficeai-474419" appears in the top navigation bar

---

### **Step 2: Navigate to OAuth Credentials**

1. In the left sidebar, click **"APIs & Services"**
2. Click **"Credentials"** from the submenu
3. You should see your OAuth 2.0 Client IDs listed

✅ **Verification:** You can see the Credentials page with existing OAuth clients

---

### **Step 3: Edit OAuth 2.0 Client ID**

1. Find your OAuth 2.0 Client ID (it will have a name like "Web client 1" or custom name)
2. Click the **pencil/edit icon** (✏️) on the right side
3. The "Edit OAuth client ID" page opens

✅ **Verification:** You see "Edit OAuth client ID" page with current settings

---

### **Step 4: Add Authorized Redirect URIs**

1. Scroll down to **"Authorized redirect URIs"** section
2. You'll see existing URIs (if any)
3. Click **"+ ADD URI"** for each new URI

**Add these URIs one by one:**

```
https://www.smartoffice-ai.com/oauth2callback
```
Click "+ ADD URI"

```
https://www.smartoffice-ai.com/calendar_oauth2callback
```
Click "+ ADD URI"

```
https://smartoffice-mogabli1.replit.app/oauth2callback
```
Click "+ ADD URI"

```
https://smartoffice-mogabli1.replit.app/calendar_oauth2callback
```

**Optional (for development/testing):**
```
https://96ee5be3-c82c-461f-815f-1879787c70fa-00-36haqnmfpcg7h.spock.replit.dev/oauth2callback
https://96ee5be3-c82c-461f-815f-1879787c70fa-00-36haqnmfpcg7h.spock.replit.dev/calendar_oauth2callback
```

✅ **Verification:** All 4-6 URIs are listed in the "Authorized redirect URIs" section

---

### **Step 5: Save Changes**

1. Scroll to the bottom of the page
2. Click the **"SAVE"** button
3. Wait for the success message (green checkmark or notification)

✅ **Verification:** You see "OAuth client updated" or similar success message

---

### **Step 6: Verify Authorized Domains**

1. Still in **APIs & Services** → **Credentials**
2. Scroll down to **"Authorized domains"** section (may be on OAuth consent screen)
3. Ensure these domains are authorized:
   - `smartoffice-ai.com`
   - `replit.app`
   - `replit.dev`

If missing, add them:
1. Go to **OAuth consent screen** (left sidebar)
2. Scroll to **"Authorized domains"**
3. Click **"+ ADD DOMAIN"**
4. Add missing domains
5. Click **"SAVE AND CONTINUE"**

✅ **Verification:** All domains are listed as authorized

---

### **Step 7: Verify OAuth Scopes**

1. Go to **OAuth consent screen** (left sidebar)
2. Scroll to **"Scopes"** section
3. Click **"EDIT"** or **"ADD OR REMOVE SCOPES"**
4. Ensure these scopes are added:

**Gmail Scope:**
```
https://www.googleapis.com/auth/gmail.readonly
```
- ✅ Read-only access to Gmail
- ✅ Allows viewing email messages and settings

**Google Calendar Scope:**
```
https://www.googleapis.com/auth/calendar.readonly
```
- ✅ Read-only access to Google Calendar
- ✅ Allows viewing calendar events

5. Click **"UPDATE"** or **"SAVE AND CONTINUE"**

✅ **Verification:** Both scopes appear in the scopes list

---

### **Step 8: Review OAuth Consent Screen**

Ensure the following information is correct:

**App Information:**
- App name: **SmartOffice AI**
- User support email: **info@smartoffice-ai.com** or your email
- App logo: (Upload if not already set - use your SO logo)

**App Domain:**
- Homepage: **https://www.smartoffice-ai.com**
- Privacy Policy: **https://www.smartoffice-ai.com/privacy**
- Terms of Service: **https://www.smartoffice-ai.com/terms**

**Developer Contact:**
- Email: **info@smartoffice-ai.com** or your email

✅ **Verification:** All app information is accurate and links work

---

### **Step 9: Check Publishing Status**

1. Still on **OAuth consent screen** page
2. Check **"Publishing status"** at the top
3. It should show:
   - **"In production"** (if already published)
   - **"Testing"** (if in review)

**If it says "Testing":**
- Add test users (your email and any test accounts)
- This allows you to test while verification is pending

✅ **Verification:** Publishing status is visible and appropriate

---

### **Step 10: Enable Required APIs**

1. Go to **APIs & Services** → **Library**
2. Search and enable these APIs (if not already enabled):

**Gmail API:**
- Search: "Gmail API"
- Click on it
- Click **"ENABLE"** (if not already enabled)

**Google Calendar API:**
- Search: "Google Calendar API"  
- Click on it
- Click **"ENABLE"** (if not already enabled)

✅ **Verification:** Both APIs show as "Enabled" with green checkmark

---

## 🔍 Final Verification Checklist

Before testing, verify all of these are complete:

- [ ] OAuth 2.0 Client ID has all redirect URIs added
- [ ] All domains are authorized (smartoffice-ai.com, replit.app, replit.dev)
- [ ] Gmail API scope (gmail.readonly) is added
- [ ] Google Calendar API scope (calendar.readonly) is added
- [ ] OAuth consent screen has correct app information
- [ ] Privacy Policy link works: https://www.smartoffice-ai.com/privacy
- [ ] Terms of Service link works: https://www.smartoffice-ai.com/terms
- [ ] Gmail API is enabled
- [ ] Google Calendar API is enabled
- [ ] Changes are saved (green success notification appeared)

---

## 🧪 Testing the Configuration

### **Test Gmail OAuth:**
1. Go to: https://www.smartoffice-ai.com
2. Register/Login
3. Click "Email" → "Connect Gmail"
4. OAuth flow should work WITHOUT "redirect_uri_mismatch" error
5. You should see Google's consent screen
6. After allowing, you should return to the app successfully

### **Test Calendar OAuth:**
1. On same account, click "Calendar" → "Connect Calendar"
2. OAuth flow should work smoothly
3. Google consent screen appears
4. After allowing, calendar events load successfully

✅ **Success:** No errors, OAuth flows complete successfully

---

## ❌ Common Errors & Fixes

### **Error: redirect_uri_mismatch**
**Cause:** Redirect URI not added to Google Cloud Console  
**Fix:** Double-check Step 4 - ensure exact URI is added (case-sensitive, with https://)

### **Error: Access blocked: This app's request is invalid**
**Cause:** Domain not authorized  
**Fix:** Go to OAuth consent screen → Add domain to "Authorized domains"

### **Error: 400 Invalid Request**
**Cause:** Scope not enabled or missing  
**Fix:** Verify Step 7 - ensure gmail.readonly and calendar.readonly are added

### **Error: API not enabled**
**Cause:** Gmail/Calendar API not enabled for project  
**Fix:** Follow Step 10 - enable both APIs in API Library

---

## 📸 Screenshot Guide (for Google)

When submitting to Google, include screenshots of:

1. **OAuth Consent Screen** - showing app name, domains, scopes
2. **Credentials Page** - showing OAuth client with all redirect URIs
3. **Enabled APIs** - showing Gmail API and Calendar API enabled
4. **Working OAuth Flow** - demo video showing successful authorization

---

## 🚨 Important Notes

⚠️ **Wait Time:** After saving changes, it may take 5-10 minutes for Google to propagate the updates globally

⚠️ **HTTPS Only:** All redirect URIs MUST use https:// (not http://)

⚠️ **Exact Match:** Redirect URIs are case-sensitive and must match exactly

⚠️ **Domain Verification:** Ensure www.smartoffice-ai.com is verified in Google Search Console

⚠️ **Test Users:** While in testing mode, add test user emails to OAuth consent screen

---

## 📧 Next Steps After Setup

1. ✅ Complete this checklist
2. ✅ Test OAuth flows (Step 3 of main task)
3. ✅ Record demo video (already created script)
4. ✅ Reply to Google with video link and confirmation
5. ✅ Wait for Google's approval (typically 3-5 business days)

---

## 🆘 Need Help?

**Google Support Resources:**
- OAuth Verification Help: https://support.google.com/cloud/answer/9110914
- Redirect URI Errors: https://developers.google.com/identity/protocols/oauth2/web-server#error-codes
- API Console Support: https://console.cloud.google.com/support

**Project-Specific Support:**
- Check application logs in Replit
- Test OAuth flow in incognito/private window
- Verify environment variables are set (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

---

**After completing this checklist, proceed to Task 3: Testing OAuth flows** ✅
