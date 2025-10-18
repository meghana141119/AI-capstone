#!/usr/bin/env python3
"""
Demo script for Emergency Communication System
Shows how the system works with dummy data
"""

import sys
import os
import csv
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SimpleEmergencySystem:
    """Simplified emergency system for demo purposes"""
    
    def __init__(self):
        self.students = self.load_students()
        self.emergency_history = []
    
    def load_students(self):
        """Load students from CSV"""
        students = []
        try:
            with open('data/students.csv', 'r') as f:
                reader = csv.DictReader(f)
                students = list(reader)
            print(f"✅ Loaded {len(students)} students")
        except Exception as e:
            print(f"❌ Error loading students: {e}")
        return students
    
    def trigger_emergency(self, emergency_type, message, branch=None, section=None):
        """Trigger emergency alert"""
        emergency_id = f"EMRG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n🚨 EMERGENCY ALERT TRIGGERED: {emergency_id}")
        print(f"Type: {emergency_type}")
        print(f"Message: {message}")
        if branch:
            print(f"Branch: {branch}")
        if section:
            print(f"Section: {section}")
        print("=" * 60)
        
        # Filter affected students
        affected_students = self.filter_students(emergency_type, branch, section)
        
        # Send notifications
        notifications_sent = self.send_notifications(emergency_id, message, affected_students)
        
        # Store in history
        emergency_record = {
            'emergency_id': emergency_id,
            'emergency_type': emergency_type,
            'message': message,
            'affected_count': len(affected_students),
            'notifications_sent': notifications_sent,
            'timestamp': datetime.now().isoformat()
        }
        self.emergency_history.append(emergency_record)
        
        print("=" * 60)
        print(f"✅ EMERGENCY RESPONSE COMPLETED")
        print(f"Emergency ID: {emergency_id}")
        print(f"Students Affected: {len(affected_students)}")
        print(f"Notifications Sent: {notifications_sent}")
        
        return emergency_record
    
    def filter_students(self, emergency_type, branch=None, section=None):
        """Filter students based on criteria"""
        if emergency_type == 'all':
            affected = self.students.copy()
        elif emergency_type == 'branch':
            affected = [s for s in self.students if s['branch'] == branch]
        elif emergency_type == 'section':
            affected = [s for s in self.students if s['branch'] == branch and s['section'] == section]
        else:
            affected = []
        
        print(f"📋 SELECTED: {len(affected)} students")
        if affected:
            print("Selected students:")
            for student in affected[:5]:  # Show first 5
                print(f"  - {student['name']} ({student['student_id']}) - {student['branch']}-{student['section']}")
            if len(affected) > 5:
                print(f"  ... and {len(affected) - 5} more")
        
        return affected
    
    def send_notifications(self, emergency_id, message, affected_students):
        """Send notifications to parents"""
        print(f"\n📧 SENDING EMERGENCY NOTIFICATIONS")
        print(f"Emergency ID: {emergency_id}")
        print(f"Affected Students: {len(affected_students)}")
        print("-" * 50)
        
        notifications_sent = 0
        for student in affected_students:
            notification = self.create_notification(emergency_id, message, student)
            self.print_email(notification)
            notifications_sent += 1
        
        print("-" * 50)
        print(f"✅ Total notifications sent: {notifications_sent}")
        return notifications_sent
    
    def create_notification(self, emergency_id, message, student):
        """Create notification for a student"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            'to': student['parent_email'],
            'subject': f"URGENT: Emergency Alert - {emergency_id}",
            'student_name': student['name'],
            'student_id': student['student_id'],
            'branch_section': f"{student['branch']}-{student['section']}",
            'emergency_message': message,
            'timestamp': timestamp
        }
    
    def print_email(self, notification):
        """Print email notification to console"""
        print(f"\n📨 EMAIL SENT:")
        print(f"To: {notification['to']}")
        print(f"Subject: {notification['subject']}")
        print(f"Student: {notification['student_name']} ({notification['student_id']})")
        print(f"Branch/Section: {notification['branch_section']}")
        print(f"Message Preview: {notification['emergency_message'][:100]}...")
        print(f"Timestamp: {notification['timestamp']}")
    
    def show_history(self):
        """Show emergency history"""
        print(f"\n📊 EMERGENCY HISTORY ({len(self.emergency_history)} emergencies)")
        print("=" * 60)
        
        for record in self.emergency_history:
            print(f"Emergency ID: {record['emergency_id']}")
            print(f"Type: {record['emergency_type']}")
            print(f"Message: {record['message']}")
            print(f"Students Affected: {record['affected_count']}")
            print(f"Notifications Sent: {record['notifications_sent']}")
            print(f"Time: {record['timestamp']}")
            print("-" * 40)
    
    def get_statistics(self):
        """Get system statistics"""
        branches = set(s['branch'] for s in self.students)
        sections = set(f"{s['branch']}-{s['section']}" for s in self.students)
        
        print(f"\n📈 SYSTEM STATISTICS")
        print("=" * 40)
        print(f"Total Students: {len(self.students)}")
        print(f"Branches: {', '.join(sorted(branches))}")
        print(f"Sections: {', '.join(sorted(sections))}")
        print(f"Total Emergencies: {len(self.emergency_history)}")
        print(f"Total Notifications Sent: {sum(r['notifications_sent'] for r in self.emergency_history)}")

def main():
    """Run the demo"""
    print("🚀 Emergency Communication System Demo")
    print("=" * 50)
    
    # Initialize system
    system = SimpleEmergencySystem()
    
    # Show statistics
    system.get_statistics()
    
    # Demo 1: Emergency for all students
    print(f"\n🔥 DEMO 1: Fire Drill for All Students")
    system.trigger_emergency('all', 'FIRE DRILL: Please evacuate the building immediately following emergency procedures.')
    
    # Demo 2: Emergency for specific branch
    print(f"\n⚡ DEMO 2: Power Outage in CSE Building")
    system.trigger_emergency('branch', 'POWER OUTAGE: CSE building is experiencing power issues. Students should move to alternate locations.', 'CSE')
    
    # Demo 3: Emergency for specific section
    print(f"\n🏥 DEMO 3: Medical Emergency in ECE-A")
    system.trigger_emergency('section', 'MEDICAL EMERGENCY: Medical assistance required in ECE-A classroom. Please stay calm and follow instructions.', 'ECE', 'A')
    
    # Show history
    system.show_history()
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"\nTo run the full web application:")
    print(f"1. Install dependencies: pip install pandas flask")
    print(f"2. Run: python app.py")
    print(f"3. Open: http://localhost:5000")

if __name__ == "__main__":
    main()

