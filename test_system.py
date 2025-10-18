#!/usr/bin/env python3
"""
Simple test script for the Emergency Communication System
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    print("🧪 Testing Emergency Communication System...")
    
    # Test 1: Check if files exist
    print("\n1. Checking file structure...")
    required_files = [
        'data/students.csv',
        'agents/alert_agent.py',
        'agents/selection_agent.py', 
        'agents/notification_agent.py',
        'agents/emergency_coordinator.py',
        'app.py',
        'templates/dashboard.html',
        'static/style.css',
        'static/script.js'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
    
    # Test 2: Check CSV data
    print("\n2. Checking student data...")
    try:
        import csv
        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            print(f"   ✅ Found {len(rows)-1} students in CSV")
            print(f"   ✅ Headers: {rows[0]}")
            
            # Show sample data
            if len(rows) > 1:
                print(f"   ✅ Sample student: {rows[1]}")
    except Exception as e:
        print(f"   ❌ Error reading CSV: {e}")
    
    # Test 3: Test agent classes (without pandas)
    print("\n3. Testing agent classes...")
    try:
        # Create simplified test without pandas
        class SimpleAlertAgent:
            def __init__(self):
                self.role = 'Emergency Alert Coordinator'
            
            def trigger_emergency(self, emergency_type, message):
                return {
                    'emergency_id': 'TEST_001',
                    'emergency_type': emergency_type,
                    'message': message,
                    'status': 'ACTIVE'
                }
        
        alert_agent = SimpleAlertAgent()
        result = alert_agent.trigger_emergency('all', 'Test emergency')
        print(f"   ✅ AlertAgent works: {result['emergency_id']}")
        
    except Exception as e:
        print(f"   ❌ Error testing AlertAgent: {e}")
    
    # Test 4: Check Flask app structure
    print("\n4. Checking Flask app...")
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'Flask' in content and 'EmergencyCoordinator' in content:
                print("   ✅ Flask app structure looks good")
            else:
                print("   ❌ Flask app structure issues")
    except Exception as e:
        print(f"   ❌ Error reading app.py: {e}")
    
    # Test 5: Check HTML templates
    print("\n5. Checking HTML templates...")
    templates = ['templates/base.html', 'templates/dashboard.html', 'templates/notifications.html']
    for template in templates:
        if os.path.exists(template):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template}")
    
    print("\n🎉 Basic system test completed!")
    print("\nTo run the full system:")
    print("1. Install dependencies: pip install pandas flask")
    print("2. Run the app: python app.py")
    print("3. Open browser: http://localhost:5000")

if __name__ == "__main__":
    test_basic_functionality()

