import pandas as pd
from datetime import datetime
import json
import os

from .alert_agent import AlertAgent
from .selection_agent import SelectionAgent
from .notification_agent import NotificationAgent

class EmergencyCoordinator:
    def __init__(self):
        self.alert_agent = AlertAgent()
        self.selection_agent = SelectionAgent()
        self.notification_agent = NotificationAgent()
        
        # Initialize emergency history storage
        self.emergency_history = []
        self.notifications_history = []
        
        # Load students data
        self.students_data = self._load_students_data()
    
    def _load_students_data(self):
        """Load students data from CSV file"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'students.csv')
            students_df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(students_df)} students from dataset")
            return students_df
        except Exception as e:
            print(f"❌ Error loading students data: {e}")
            return pd.DataFrame()
    
    def trigger_emergency(self, emergency_type, emergency_message, branch=None, section=None, selected_students=None):
        """
        Main method to trigger emergency and coordinate all agents
        
        Args:
            emergency_type: 'all', 'branch', or 'section'
            emergency_message: Description of the emergency
            branch: Branch name (required for branch/section emergencies)
            section: Section name (required for section emergencies)
            selected_students: List of student IDs who are safe (checked) - alerts will be sent to unchecked students
        
        Returns:
            dict: Complete emergency response details
        """
        print(f"\n🚨 INITIATING EMERGENCY RESPONSE")
        print(f"Type: {emergency_type}")
        print(f"Message: {emergency_message}")
        if branch:
            print(f"Branch: {branch}")
        if section:
            print(f"Section: {section}")
        print("=" * 60)
        
        # Step 1: Alert Agent - Trigger the emergency
        alert_data = self.alert_agent.trigger_emergency(
            emergency_type, emergency_message, self.students_data
        )
        
        # Step 2: Selection Agent - Filter affected students
        filter_criteria = {
            'emergency_type': emergency_type,
            'branch': branch,
            'section': section,
            'selected_students': selected_students or []  # Safe students (checked)
        }
        
        affected_students = self.selection_agent.filter_students(
            self.students_data, filter_criteria
        )
        
        # Update alert data with affected students
        alert_data['affected_students'] = affected_students.to_dict('records')
        alert_data['affected_count'] = len(affected_students)
        
        # Step 3: Notification Agent - Send notifications
        notification_result = self.notification_agent.send_emergency_notifications(
            alert_data, affected_students
        )
        
        # Store emergency in history
        emergency_record = {
            'alert_data': alert_data,
            'notification_result': notification_result,
            'timestamp': datetime.now().isoformat()
        }
        self.emergency_history.append(emergency_record)
        self.notifications_history.extend(notification_result.get('details', []))
        
        # Prepare response
        response = {
            'emergency_id': alert_data['emergency_id'],
            'status': 'completed',
            'emergency_type': emergency_type,
            'emergency_message': emergency_message,
            'affected_students_count': len(affected_students),
            'notifications_sent': notification_result.get('notifications_sent', 0),
            'timestamp': datetime.now().isoformat(),
            'details': {
                'alert_data': alert_data,
                'affected_students': affected_students.to_dict('records'),
                'notification_result': notification_result
            }
        }
        
        print("=" * 60)
        print(f"✅ EMERGENCY RESPONSE COMPLETED")
        print(f"Emergency ID: {response['emergency_id']}")
        print(f"Students Affected: {response['affected_students_count']}")
        print(f"Notifications Sent: {response['notifications_sent']}")
        
        return response
    
    def get_emergency_history(self):
        """Get history of all emergencies"""
        return self.emergency_history
    
    def get_recent_notifications(self, limit=10):
        """Get recent notifications"""
        return self.notifications_history[-limit:] if self.notifications_history else []
    
    def get_available_branches(self):
        """Get list of available branches"""
        return self.selection_agent.get_available_branches(self.students_data)
    
    def get_available_sections(self, branch=None):
        """Get list of available sections"""
        return self.selection_agent.get_available_sections(self.students_data, branch)
    
    def get_students_for_branch_section(self, branch, section=None):
        """Get students for a specific branch and section"""
        filtered_students = self.students_data.copy()
        
        # Filter by branch
        filtered_students = filtered_students[filtered_students['branch'] == branch]
        
        # Filter by section if provided
        if section:
            filtered_students = filtered_students[filtered_students['section'] == section]
        
        return filtered_students.to_dict('records')
    
    def send_status_update(self, emergency_id, update_message):
        """Send status update for existing emergency"""
        # Find the emergency in history
        emergency = None
        for record in self.emergency_history:
            if record['alert_data']['emergency_id'] == emergency_id:
                emergency = record['alert_data']
                break
        
        if not emergency:
            return {'status': 'error', 'message': 'Emergency not found'}
        
        update_result = self.notification_agent.send_status_update(emergency, update_message)
        return update_result
