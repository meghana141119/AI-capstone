import pandas as pd
from datetime import datetime

class AlertAgent:
    def __init__(self):
        self.role = 'Emergency Alert Coordinator'
        self.goal = 'Trigger emergency alerts and coordinate response'
        self.backstory = 'You are responsible for initiating emergency communication protocols and ensuring all stakeholders are notified promptly.'
    
    def trigger_emergency(self, emergency_type, emergency_message, students_data):
        """
        Trigger emergency alert based on type and message
        
        Args:
            emergency_type: 'all', 'branch', or 'section'
            emergency_message: Description of the emergency
            students_data: DataFrame containing student information
        
        Returns:
            dict: Emergency alert details
        """
        alert_data = {
            'emergency_id': f"EMRG_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'emergency_type': emergency_type,
            'emergency_message': emergency_message,
            'timestamp': datetime.now().isoformat(),
            'status': 'ACTIVE',
            'affected_students': []
        }
        
        # Determine affected students based on emergency type
        if emergency_type == 'all':
            alert_data['affected_students'] = students_data.to_dict('records')
            alert_data['target_description'] = "All Students"
        elif emergency_type == 'branch':
            # This will be handled by SelectionAgent
            alert_data['target_description'] = "Specific Branch"
        elif emergency_type == 'section':
            # This will be handled by SelectionAgent
            alert_data['target_description'] = "Specific Section"
        
        print(f"🚨 EMERGENCY ALERT TRIGGERED: {alert_data['emergency_id']}")
        print(f"Type: {emergency_type}")
        print(f"Message: {emergency_message}")
        print(f"Timestamp: {alert_data['timestamp']}")
        
        return alert_data
