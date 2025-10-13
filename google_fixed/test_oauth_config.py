#!/usr/bin/env python3
"""
Test OAuth Configuration - Verify Redirect URIs
This script checks if OAuth redirect URIs are correctly configured
"""

import os
import sys

def test_oauth_config():
    """Test OAuth configuration and display redirect URIs"""
    
    print("=" * 70)
    print("🔍 OAUTH CONFIGURATION TEST - SmartOffice AI")
    print("=" * 70)
    print()
    
    # Check environment variables
    print("📋 Step 1: Checking Environment Variables")
    print("-" * 70)
    
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    if google_client_id:
        print(f"✅ GOOGLE_CLIENT_ID: Set (ends with ...{google_client_id[-20:]})")
    else:
        print("❌ GOOGLE_CLIENT_ID: NOT SET")
        
    if google_client_secret:
        print(f"✅ GOOGLE_CLIENT_SECRET: Set (length: {len(google_client_secret)} chars)")
    else:
        print("❌ GOOGLE_CLIENT_SECRET: NOT SET")
    
    print()
    
    # Determine deployment domains
    print("📋 Step 2: Determining Deployment Domains")
    print("-" * 70)
    
    # Check for Replit domains
    replit_domains = os.environ.get('REPLIT_DOMAINS', '')
    replit_dev_domain = os.environ.get('REPLIT_DEV_DOMAIN', '')
    
    domains = []
    
    # Production domain
    production_domain = "www.smartoffice-ai.com"
    domains.append(("Production", production_domain))
    print(f"✅ Production Domain: https://{production_domain}")
    
    # Replit deployment domain
    replit_app_domain = "smartoffice-mogabli1.replit.app"
    domains.append(("Replit App", replit_app_domain))
    print(f"✅ Replit App Domain: https://{replit_app_domain}")
    
    # Development domain
    if replit_dev_domain:
        domains.append(("Development", replit_dev_domain))
        print(f"✅ Development Domain: https://{replit_dev_domain}")
    
    print()
    
    # Generate redirect URIs
    print("📋 Step 3: Required Redirect URIs for Google Cloud Console")
    print("-" * 70)
    print()
    print("Copy and paste these URIs into Google Cloud Console:")
    print("(APIs & Services → Credentials → OAuth 2.0 Client ID → Edit)")
    print()
    
    all_uris = []
    
    for domain_type, domain in domains:
        print(f"### {domain_type} Domain ###")
        gmail_uri = f"https://{domain}/oauth2callback"
        calendar_uri = f"https://{domain}/calendar_oauth2callback"
        
        print(f"  {gmail_uri}")
        print(f"  {calendar_uri}")
        print()
        
        all_uris.append(gmail_uri)
        all_uris.append(calendar_uri)
    
    # Summary
    print("=" * 70)
    print("📝 SUMMARY: All Redirect URIs")
    print("=" * 70)
    for i, uri in enumerate(all_uris, 1):
        print(f"{i}. {uri}")
    
    print()
    print("=" * 70)
    print("✅ Total URIs to add: ", len(all_uris))
    print("=" * 70)
    print()
    
    # OAuth Scopes
    print("📋 Step 4: Required OAuth Scopes")
    print("-" * 70)
    print()
    print("Gmail Scope:")
    print("  https://www.googleapis.com/auth/gmail.readonly")
    print()
    print("Google Calendar Scope:")
    print("  https://www.googleapis.com/auth/calendar.readonly")
    print()
    
    # Configuration status
    print("=" * 70)
    print("📊 CONFIGURATION STATUS")
    print("=" * 70)
    
    if google_client_id and google_client_secret:
        print("✅ OAuth credentials are configured")
        print("✅ Redirect URIs generated successfully")
        print()
        print("🎯 NEXT STEPS:")
        print("1. Copy all redirect URIs above")
        print("2. Add them to Google Cloud Console (project: smartofficeai-474419)")
        print("3. Save changes in Google Cloud Console")
        print("4. Wait 5-10 minutes for changes to propagate")
        print("5. Test OAuth flow by clicking 'Connect Gmail' in the app")
    else:
        print("⚠️  OAuth credentials missing!")
        print()
        print("🛠️  TO FIX:")
        print("1. Go to Google Cloud Console")
        print("2. Get your OAuth Client ID and Client Secret")
        print("3. Add them as Replit Secrets:")
        print("   - GOOGLE_CLIENT_ID=your_client_id")
        print("   - GOOGLE_CLIENT_SECRET=your_client_secret")
    
    print()
    print("=" * 70)
    print()

if __name__ == "__main__":
    test_oauth_config()
