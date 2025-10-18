# 🚀 Quick Start Guide

## Emergency Communication System

This is a simple emergency communication system that demonstrates how to use AI agents to manage emergency alerts and notifications.

## 🎯 What It Does

- **Triggers Emergency Alerts**: Send alerts to all students, specific branches, or specific sections
- **AI Agent Workflow**: Uses three specialized agents to handle the emergency process
- **Parent Notifications**: Sends formatted email notifications to parents (printed to console)
- **Web Dashboard**: Simple HTML/CSS interface for managing emergencies
- **Real-time Tracking**: Monitor active emergencies and notification history

## 📁 Project Structure

```
emergency_communication_system/
├── agents/                    # AI Agent implementations
│   ├── alert_agent.py        # Triggers emergency alerts
│   ├── selection_agent.py    # Filters students by criteria
│   ├── notification_agent.py # Sends notifications to parents
│   └── emergency_coordinator.py # Orchestrates all agents
├── templates/                # HTML templates
│   ├── dashboard.html        # Main dashboard
│   └── notifications.html    # Notifications page
├── static/                   # CSS and JavaScript
├── data/
│   └── students.csv         # Student dataset (20 students)
├── app.py                   # Flask web application
├── demo.py                  # Command-line demo
└── test_system.py          # System tests
```

## ⚡ Quick Demo (No Dependencies)

Run the command-line demo to see how the system works:

```bash
python demo.py
```

This will:
1. Load 20 dummy students from CSV
2. Trigger 3 different types of emergencies
3. Show how notifications are sent to parents
4. Display emergency history and statistics

## 🌐 Web Application

### 1. Install Dependencies
```bash
pip install pandas flask
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open Browser
- **Dashboard**: http://localhost:5000
- **Notifications**: http://localhost:5000/notifications

## 🎮 How to Use

### Web Interface

1. **Dashboard** (`http://localhost:5000`):
   - View current emergency status
   - Trigger new emergency alerts
   - Use quick action buttons for common emergencies
   - See recent activity

2. **Trigger Emergency**:
   - Select emergency type: All/Branch/Section
   - Choose branch and section (if applicable)
   - Enter emergency message
   - Click "Send Emergency Alert"

3. **Notifications Page** (`http://localhost:5000/notifications`):
   - View emergency history
   - See all notifications sent
   - Check system statistics

### API Usage

You can also trigger emergencies via API:

```bash
# Emergency for all students
curl -X POST http://localhost:5000/api/emergency/trigger \
  -H "Content-Type: application/json" \
  -d '{"emergency_type": "all", "emergency_message": "Fire drill in progress"}'

# Emergency for CSE branch
curl -X POST http://localhost:5000/api/emergency/trigger \
  -H "Content-Type: application/json" \
  -d '{"emergency_type": "branch", "branch": "CSE", "emergency_message": "Power outage in CSE building"}'

# Emergency for ECE-A section
curl -X POST http://localhost:5000/api/emergency/trigger \
  -H "Content-Type: application/json" \
  -d '{"emergency_type": "section", "branch": "ECE", "section": "A", "emergency_message": "Medical emergency in ECE-A classroom"}'
```

## 📊 Sample Data

The system includes 20 dummy students across 4 branches:

- **CSE** (Computer Science): Sections A, B, C (5 students)
- **ECE** (Electronics): Sections A, B, C (5 students)  
- **MECH** (Mechanical): Sections A, B, C (5 students)
- **CIVIL** (Civil): Sections A, B, C (5 students)

Each student has:
- Student ID
- Name
- Branch and Section
- Parent email address

## 🤖 AI Agents Explained

### AlertAgent
- **Role**: Emergency Alert Coordinator
- **Function**: Triggers emergency alerts and generates unique emergency IDs
- **Output**: Emergency alert details with timestamp and status

### SelectionAgent
- **Role**: Student Selection Specialist
- **Function**: Filters students based on emergency criteria (all/branch/section)
- **Output**: List of affected students matching the criteria

### NotificationAgent
- **Role**: Emergency Notification Specialist
- **Function**: Sends formatted email notifications to parents
- **Output**: Email notifications (printed to console in demo)

### EmergencyCoordinator
- **Role**: System Orchestrator
- **Function**: Coordinates all agents and manages the complete workflow
- **Output**: Complete emergency response with all details

## 🔧 Testing

Run the system test to verify everything works:

```bash
python test_system.py
```

This checks:
- ✅ All files exist
- ✅ Student data loads correctly
- ✅ Agent classes work
- ✅ Flask app structure
- ✅ HTML templates

## 📝 Example Output

When you trigger an emergency, you'll see output like this:

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

## 🚀 Next Steps

1. **Try the Demo**: Run `python demo.py` to see the system in action
2. **Test the Web App**: Install dependencies and run `python app.py`
3. **Explore the Code**: Look at the agent implementations in the `agents/` folder
4. **Customize**: Modify the student data or add new features

## 🔍 Key Features Demonstrated

- **Agent-based Architecture**: Shows how AI agents can work together
- **Data Filtering**: Demonstrates intelligent student selection
- **Emergency Management**: Complete emergency response workflow
- **Web Interface**: Simple HTML/CSS dashboard
- **API Integration**: RESTful API for programmatic access
- **Real-time Updates**: Dynamic status updates and notifications

## 💡 Learning Outcomes

This project demonstrates:
- AI agent coordination and workflow management
- Data filtering and selection algorithms
- Web application development with Flask
- Emergency communication system design
- API development and integration
- User interface design for emergency management

---

**Ready to get started?** Run `python demo.py` to see the system in action! 🎉

