# Emergency Communication System

A simple emergency communication system built with Flask and CrewAI agents to manage emergency alerts and notifications to parents.

## Features

- **Emergency Alert System**: Trigger alerts for all students, specific branches, or specific sections
- **CrewAI Agents**: Three specialized agents manage the workflow:
  - **AlertAgent**: Triggers emergency alerts
  - **SelectionAgent**: Filters students by criteria
  - **NotificationAgent**: Sends formatted updates to parents
- **Web Dashboard**: Simple HTML/CSS interface for emergency management
- **Real-time Status**: Track active emergencies and recent notifications
- **Dummy Data**: Includes sample student data for testing

## Project Structure

```
emergency_communication_system/
├── agents/
│   ├── __init__.py
│   ├── alert_agent.py          # Emergency alert coordinator
│   ├── selection_agent.py      # Student filtering specialist
│   ├── notification_agent.py   # Notification sender
│   └── emergency_coordinator.py # Main orchestrator
├── templates/
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard
│   └── notifications.html     # Notifications page
├── static/
│   ├── style.css             # Main stylesheet
│   └── script.js             # JavaScript functionality
├── data/
│   └── students.csv          # Student dataset
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   - Dashboard: http://localhost:5000
   - Notifications: http://localhost:5000/notifications

3. **Trigger an emergency**:
   - Use the form on the dashboard
   - Select emergency type (All/Branch/Section)
   - Enter emergency message
   - Click "Send Emergency Alert"

## Sample Data

The system includes 20 dummy students across 4 branches:
- **CSE** (Computer Science): Sections A, B, C
- **ECE** (Electronics): Sections A, B, C  
- **MECH** (Mechanical): Sections A, B, C
- **CIVIL** (Civil): Sections A, B, C

Each student has:
- Student ID
- Name
- Branch and Section
- Parent email address

## API Endpoints

- `POST /api/emergency/trigger` - Trigger emergency alert
- `GET /api/emergency/status` - Get current emergency status
- `GET /api/emergency/history` - Get emergency history
- `GET /api/notifications/recent` - Get recent notifications
- `POST /api/emergency/resolve` - Resolve current emergency
- `GET /api/branches` - Get available branches
- `GET /api/sections?branch=X` - Get sections for branch

## Example Usage

### Trigger Emergency for All Students
```bash
curl -X POST http://localhost:5000/api/emergency/trigger \
  -H "Content-Type: application/json" \
  -d '{"emergency_type": "all", "emergency_message": "Fire drill in progress"}'
```

### Trigger Emergency for Specific Branch
```bash
curl -X POST http://localhost:5000/api/emergency/trigger \
  -H "Content-Type: application/json" \
  -d '{"emergency_type": "branch", "branch": "CSE", "emergency_message": "Power outage in CSE building"}'
```

### Trigger Emergency for Specific Section
```bash
curl -X POST http://localhost:5000/api/emergency/trigger \
  -H "Content-Type: application/json" \
  -d '{"emergency_type": "section", "branch": "ECE", "section": "A", "emergency_message": "Medical emergency in ECE-A classroom"}'
```

## CrewAI Agents

### AlertAgent
- Role: Emergency Alert Coordinator
- Responsibilities: Trigger emergency alerts and coordinate response
- Input: Emergency type, message, student data
- Output: Emergency alert details with unique ID and timestamp

### SelectionAgent  
- Role: Student Selection Specialist
- Responsibilities: Filter students based on emergency criteria
- Input: Student data, filter criteria (branch/section)
- Output: Filtered list of affected students

### NotificationAgent
- Role: Emergency Notification Specialist  
- Responsibilities: Send formatted emergency updates to parents
- Input: Alert data, affected students
- Output: Email notifications (printed to console)

## Emergency Workflow

1. **Emergency Triggered**: User triggers emergency via web interface or API
2. **Alert Generated**: AlertAgent creates emergency alert with unique ID
3. **Students Selected**: SelectionAgent filters students based on criteria
4. **Notifications Sent**: NotificationAgent sends formatted emails to parents
5. **Status Updated**: Dashboard shows active emergency status
6. **Emergency Resolved**: User can resolve emergency when situation is clear

## Testing

The system includes dummy email functionality that prints notifications to the console. In a production environment, you would integrate with a real SMTP service.

Example console output:
```
🚨 EMERGENCY ALERT TRIGGERED: EMRG_20240927_102630
Type: section
Message: Fire in CSE-A classroom
Timestamp: 2024-09-27T10:26:30

📋 SELECTED: 2 students from CSE-A
Selected students:
  - John Smith (1001) - CSE-A
  - Sarah Johnson (1002) - CSE-A

📧 SENDING EMERGENCY NOTIFICATIONS
Emergency ID: EMRG_20240927_102630
Affected Students: 2
--------------------------------------------------

📨 EMAIL SENT:
To: john.smith.parent@email.com
Subject: URGENT: Emergency Alert - EMRG_20240927_102630
Message: [Formatted emergency message]
Student: John Smith (1001)
Branch/Section: CSE-A

📨 EMAIL SENT:
To: sarah.johnson.parent@email.com
Subject: URGENT: Emergency Alert - EMRG_20240927_102630
Message: [Formatted emergency message]
Student: Sarah Johnson (1002)
Branch/Section: CSE-A

--------------------------------------------------
✅ Total notifications sent: 2
```

## Security Notes

- This is a demo system with dummy data
- No real email sending is implemented
- No authentication or authorization
- Not suitable for production use without proper security measures

## Future Enhancements

- Real SMTP integration
- User authentication
- SMS notifications
- Emergency status updates
- Mobile app interface
- Database integration
- Audit logging
- Multi-language support

