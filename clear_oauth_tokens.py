#!/usr/bin/env python3
"""
Clear OAuth tokens for a user - allows re-authorization for demo recording
"""

import sqlite3
import sys

def clear_tokens(email):
    """Clear Gmail and Calendar OAuth tokens for a user"""
    conn = sqlite3.connect('smartoffice.db')
    cursor = conn.cursor()
    
    # Find user
    cursor.execute("SELECT id, email FROM users WHERE email = ?;", (email,))
    user = cursor.fetchone()
    
    if not user:
        print(f"❌ User not found: {email}")
        conn.close()
        return False
    
    user_id, user_email = user
    print(f"Found user: {user_email} (ID: {user_id})")
    
    # Delete Gmail tokens
    cursor.execute("DELETE FROM gmail_tokens WHERE user_id = ?;", (user_id,))
    gmail_deleted = cursor.rowcount
    
    # Delete Calendar tokens
    cursor.execute("DELETE FROM calendar_tokens WHERE user_id = ?;", (user_id,))
    calendar_deleted = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Cleared OAuth tokens:")
    print(f"   - Gmail tokens deleted: {gmail_deleted}")
    print(f"   - Calendar tokens deleted: {calendar_deleted}")
    print(f"\n🎬 You can now re-authorize {user_email} for fresh demo recording!")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🧹 CLEAR OAUTH TOKENS FOR DEMO RECORDING")
    print("=" * 60)
    print()
    
    # Show available users
    conn = sqlite3.connect('smartoffice.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users;")
    users = cursor.fetchall()
    conn.close()
    
    print("Available users:")
    for user_id, email in users:
        print(f"  {user_id}. {email}")
    print()
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Enter email to clear tokens: ").strip()
    
    clear_tokens(email)
    print()
    print("=" * 60)
