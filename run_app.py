#!/usr/bin/env python3
"""
Simple script to run the Flask app with error handling
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("🚀 Starting Emergency Communication System...")
    print("📊 Dashboard: http://localhost:5000")
    print("📧 Notifications: http://localhost:5000/notifications")
    print("🔧 API Documentation:")
    print("  - POST /api/emergency/trigger - Trigger emergency")
    print("  - GET /api/emergency/status - Get current status")
    print("  - GET /api/emergency/history - Get emergency history")
    print("  - GET /api/notifications/recent - Get recent notifications")
    print("  - POST /api/emergency/resolve - Resolve emergency")
    print("=" * 50)
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install pandas flask")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check the error details above.")

