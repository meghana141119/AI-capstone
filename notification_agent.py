import pandas as pd
from datetime import datetime

class NotificationAgent:
    def __init__(self):
        self.role = 'Emergency Notification Specialist'
        self.goal = 'Send formatted emergency updates to parents and stakeholders'
        self.backstory = 'You are responsible for crafting and delivering clear, concise emergency notifications to parents and ensuring proper communication protocols are followed.'
    
    def send_emergency_notifications(self, alert_data, affected_students):
        """
        Send emergency notifications to parents of affected students
        
        Args:
            alert_data: dict containing emergency alert information
            affected_students: DataFrame containing affected student information
        
        Returns:
            dict: Notification results
        """
        notifications_sent = []
        
        if affected_students.empty:
            print("⚠️ No students to notify")
            return {'status': 'no_students', 'notifications_sent': 0}
        
        print(f"\n📧 SENDING EMERGENCY NOTIFICATIONS")
        print(f"Emergency ID: {alert_data['emergency_id']}")
        print(f"Affected Students: {len(affected_students)}")
        print("-" * 50)
        
        for _, student in affected_students.iterrows():
            notification = self._create_notification(alert_data, student)
            notifications_sent.append(notification)
            
            # Simulate sending email (print to console)
            print(f"\n📨 EMAIL SENT:")
            print(f"To: {student['parent_email']}")
            print(f"Subject: {notification['subject']}")
            print(f"Message: {notification['message']}")
            print(f"Student: {student['name']} ({student['student_id']})")
            print(f"Branch/Section: {student['branch']}-{student['section']}")
        
        print("-" * 50)
        print(f"✅ Total notifications sent: {len(notifications_sent)}")
        
        return {
            'status': 'success',
            'notifications_sent': len(notifications_sent),
            'details': notifications_sent
        }
    
    def _create_notification(self, alert_data, student):
        """Create a formatted notification for a specific student"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        subject = f"URGENT: Emergency Alert - {alert_data['emergency_id']}"
        
        message = f"""
Dear Parent/Guardian of {student['name']},

URGENT EMERGENCY NOTIFICATION

Emergency ID: {alert_data['emergency_id']}
Time: {timestamp}
Student: {student['name']} (ID: {student['student_id']})
Branch/Section: {student['branch']}-{student['section']}

EMERGENCY DETAILS:
{alert_data['emergency_message']}

PLEASE TAKE IMMEDIATE ACTION:
- Ensure your child's safety
- Follow official emergency procedures
- Stay tuned for further updates
- Contact the school if you have any concerns

This is an automated emergency notification system.
Please do not reply to this email.

School Emergency Communication System
Generated at: {timestamp}

---
This message was sent to all parents of affected students.
        """.strip()
        
        return {
            'student_id': student['student_id'],
            'parent_email': student['parent_email'],
            'subject': subject,
            'message': message,
            'timestamp': timestamp,
            'status': 'sent'
        }
    
    def send_status_update(self, alert_data, update_message):
        """Send status update for ongoing emergency"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n📢 EMERGENCY STATUS UPDATE")
        print(f"Emergency ID: {alert_data['emergency_id']}")
        print(f"Time: {timestamp}")
        print(f"Update: {update_message}")
        print("-" * 50)
        
        return {
            'emergency_id': alert_data['emergency_id'],
            'update_message': update_message,
            'timestamp': timestamp,
            'status': 'update_sent'
        }
