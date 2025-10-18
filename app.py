from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import sys

# Add the current directory to Python path to import agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.emergency_coordinator import EmergencyCoordinator

app = Flask(__name__)

# Initialize the emergency coordinator
emergency_coordinator = EmergencyCoordinator()

# Store current emergency status
current_emergency_status = {
    'active': False,
    'emergency_id': None,
    'emergency_message': None,
    'emergency_type': None,
    'timestamp': None
}

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html', 
                         emergency_status=current_emergency_status,
                         available_branches=emergency_coordinator.get_available_branches())

@app.route('/api/emergency/trigger', methods=['POST'])
def trigger_emergency():
    """API endpoint to trigger emergency alerts"""
    try:
        data = request.get_json()
        
        emergency_type = data.get('emergency_type', 'all')
        emergency_message = data.get('emergency_message', 'General emergency alert')
        branch = data.get('branch')
        section = data.get('section')
        selected_students = data.get('selected_students', [])  # List of student IDs who are safe (checked)
        
        # Validate input
        if emergency_type not in ['all', 'branch', 'section']:
            return jsonify({'error': 'Invalid emergency type'}), 400
        
        if emergency_type in ['branch', 'section'] and not branch:
            return jsonify({'error': 'Branch is required for branch/section emergencies'}), 400
        
        if emergency_type == 'section' and not section:
            return jsonify({'error': 'Section is required for section emergencies'}), 400
        
        # Trigger emergency
        response = emergency_coordinator.trigger_emergency(
            emergency_type, emergency_message, branch, section, selected_students
        )
        
        # Update current emergency status
        current_emergency_status.update({
            'active': True,
            'emergency_id': response['emergency_id'],
            'emergency_message': emergency_message,
            'emergency_type': emergency_type,
            'timestamp': response['timestamp']
        })
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emergency/status')
def get_emergency_status():
    """Get current emergency status"""
    return jsonify(current_emergency_status)

@app.route('/api/emergency/history')
def get_emergency_history():
    """Get emergency history"""
    history = emergency_coordinator.get_emergency_history()
    return jsonify(history)

@app.route('/api/notifications/recent')
def get_recent_notifications():
    """Get recent notifications"""
    notifications = emergency_coordinator.get_recent_notifications()
    return jsonify(notifications)

@app.route('/api/branches')
def get_branches():
    """Get available branches"""
    branches = emergency_coordinator.get_available_branches()
    return jsonify(branches)

@app.route('/api/sections')
def get_sections():
    """Get sections for a specific branch"""
    branch = request.args.get('branch')
    sections = emergency_coordinator.get_available_sections(branch)
    return jsonify(sections)

@app.route('/api/students')
def get_students():
    """Get students for a specific branch and section"""
    branch = request.args.get('branch')
    section = request.args.get('section')
    
    if not branch:
        return jsonify({'error': 'Branch is required'}), 400
    
    students = emergency_coordinator.get_students_for_branch_section(branch, section)
    return jsonify(students)

@app.route('/api/emergency/resolve', methods=['POST'])
def resolve_emergency():
    """Resolve current emergency"""
    global current_emergency_status
    
    current_emergency_status = {
        'active': False,
        'emergency_id': None,
        'emergency_message': None,
        'emergency_type': None,
        'timestamp': None
    }
    
    return jsonify({'status': 'emergency_resolved', 'message': 'Emergency status cleared'})

@app.route('/api/emergency/update', methods=['POST'])
def send_status_update():
    """Send status update for current emergency"""
    try:
        data = request.get_json()
        emergency_id = data.get('emergency_id')
        update_message = data.get('update_message')
        
        if not emergency_id or not update_message:
            return jsonify({'error': 'Emergency ID and update message are required'}), 400
        
        result = emergency_coordinator.send_status_update(emergency_id, update_message)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/notifications')
def notifications_page():
    """Notifications page"""
    recent_notifications = emergency_coordinator.get_recent_notifications()
    emergency_history = emergency_coordinator.get_emergency_history()
    
    return render_template('notifications.html',
                         notifications=recent_notifications,
                         emergency_history=emergency_history)

@app.route('/test')
def test_page():
    """Test page for debugging"""
    with open('test_students.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
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
    
    app.run(debug=True, host='0.0.0.0', port=5000)

