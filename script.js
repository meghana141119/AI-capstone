// Emergency Communication System JavaScript

// Global variables
let currentEmergencyStatus = null;

// Initialize the dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadEmergencyStatus();
    loadRecentActivity();
});

// Load current emergency status
async function loadEmergencyStatus() {
    try {
        const response = await fetch('/api/emergency/status');
        currentEmergencyStatus = await response.json();
        updateEmergencyStatusDisplay();
    } catch (error) {
        console.error('Error loading emergency status:', error);
        showMessage('Error loading emergency status', 'error');
    }
}

// Update emergency status display
function updateEmergencyStatusDisplay() {
    const statusSection = document.querySelector('.status-section');
    if (!statusSection) return;

    if (currentEmergencyStatus && currentEmergencyStatus.active) {
        statusSection.innerHTML = `
            <div class="status-card emergency-active">
                <div class="status-header">
                    <i class="fas fa-shield-alt"></i>
                    <h2>Emergency Status</h2>
                </div>
                <div class="status-content">
                    <div class="emergency-indicator active">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>EMERGENCY ACTIVE</span>
                    </div>
                    <div class="emergency-details">
                        <p><strong>Emergency ID:</strong> ${currentEmergencyStatus.emergency_id}</p>
                        <p><strong>Type:</strong> ${currentEmergencyStatus.emergency_type}</p>
                        <p><strong>Message:</strong> ${currentEmergencyStatus.emergency_message}</p>
                        <p><strong>Time:</strong> ${new Date(currentEmergencyStatus.timestamp).toLocaleString()}</p>
                    </div>
                    <button onclick="resolveEmergency()" class="btn btn-danger">
                        <i class="fas fa-check-circle"></i> Resolve Emergency
                    </button>
                </div>
            </div>
        `;
    } else {
        statusSection.innerHTML = `
            <div class="status-card emergency-inactive">
                <div class="status-header">
                    <i class="fas fa-shield-alt"></i>
                    <h2>Emergency Status</h2>
                </div>
                <div class="status-content">
                    <div class="emergency-indicator inactive">
                        <i class="fas fa-check-circle"></i>
                        <span>ALL CLEAR</span>
                    </div>
                    <p>No active emergencies at this time.</p>
                </div>
            </div>
        `;
    }
}

// Load recent activity
async function loadRecentActivity() {
    try {
        const response = await fetch('/api/notifications/recent');
        const notifications = await response.json();
        displayRecentActivity(notifications);
    } catch (error) {
        console.error('Error loading recent activity:', error);
        const activityDiv = document.getElementById('recentActivity');
        if (activityDiv) {
            activityDiv.innerHTML = '<p>Error loading recent activity.</p>';
        }
    }
}

// Display recent activity
function displayRecentActivity(notifications) {
    const activityDiv = document.getElementById('recentActivity');
    if (!activityDiv) return;

    if (notifications && notifications.length > 0) {
        const activityHTML = notifications.slice(0, 5).map(notification => `
            <div class="activity-item">
                <i class="fas fa-envelope"></i>
                <div class="activity-content">
                    <p><strong>${notification.subject}</strong></p>
                    <p>Sent to ${notification.parent_email}</p>
                    <small>${new Date(notification.timestamp).toLocaleString()}</small>
                </div>
            </div>
        `).join('');
        
        activityDiv.innerHTML = `
            <div class="activity-list">
                ${activityHTML}
            </div>
            <a href="/notifications" class="btn btn-primary">
                <i class="fas fa-eye"></i> View All Notifications
            </a>
        `;
    } else {
        activityDiv.innerHTML = '<p>No recent activity to display.</p>';
    }
}

// Toggle form filters based on emergency type
function toggleFilters() {
    const emergencyType = document.getElementById('emergencyType').value;
    const branchGroup = document.getElementById('branchGroup');
    const sectionGroup = document.getElementById('sectionGroup');
    const studentSelectionGroup = document.getElementById('studentSelectionGroup');
    
    if (emergencyType === 'all') {
        branchGroup.style.display = 'none';
        sectionGroup.style.display = 'none';
        studentSelectionGroup.style.display = 'none';
    } else if (emergencyType === 'branch') {
        branchGroup.style.display = 'block';
        sectionGroup.style.display = 'none';
        studentSelectionGroup.style.display = 'none';
    } else if (emergencyType === 'section') {
        branchGroup.style.display = 'block';
        sectionGroup.style.display = 'block';
        // Student selection will be shown when both branch and section are selected
    }
}

// Load sections for selected branch
async function loadSections() {
    const branch = document.getElementById('branch').value;
    const sectionSelect = document.getElementById('section');
    const studentSelectionGroup = document.getElementById('studentSelectionGroup');
    
    if (!branch) {
        sectionSelect.innerHTML = '<option value="">Select Section</option>';
        studentSelectionGroup.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/sections?branch=${encodeURIComponent(branch)}`);
        const sections = await response.json();
        
        sectionSelect.innerHTML = '<option value="">Select Section</option>';
        sections.forEach(section => {
            const option = document.createElement('option');
            option.value = section;
            option.textContent = section;
            sectionSelect.appendChild(option);
        });
        
        // Hide student selection until section is also selected
        studentSelectionGroup.style.display = 'none';
        
        // Add change event listener to load students when section is selected
        sectionSelect.onchange = loadStudents;
    } catch (error) {
        console.error('Error loading sections:', error);
        showMessage('Error loading sections', 'error');
    }
}

// Load students for selected branch and section
async function loadStudents() {
    const branch = document.getElementById('branch').value;
    const section = document.getElementById('section').value;
    const studentSelectionGroup = document.getElementById('studentSelectionGroup');
    const studentChecklist = document.getElementById('studentChecklist');
    
    if (!branch || !section) {
        studentSelectionGroup.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/students?branch=${encodeURIComponent(branch)}&section=${encodeURIComponent(section)}`);
        const students = await response.json();
        
        if (students && students.length > 0) {
            displayStudentChecklist(students);
            studentSelectionGroup.style.display = 'block';
        } else {
            studentChecklist.innerHTML = '<p>No students found for the selected branch and section.</p>';
            studentSelectionGroup.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading students:', error);
        showMessage('Error loading students', 'error');
        studentSelectionGroup.style.display = 'none';
    }
}

// Display student checklist with all students checked by default
function displayStudentChecklist(students) {
    const studentChecklist = document.getElementById('studentChecklist');
    
    const checklistHTML = `
        <div class="student-checklist-header">
            <h4>Students (${students.length} total)</h4>
            <div class="checklist-controls">
                <button onclick="selectAllStudents()">Select All (Safe)</button>
                <button onclick="deselectAllStudents()">Deselect All (In Danger)</button>
            </div>
        </div>
        <div id="studentList">
            ${students.map(student => `
                <div class="student-item">
                    <input type="checkbox" 
                           id="student_${student.student_id}" 
                           value="${student.student_id}" 
                           checked 
                           onchange="updateStudentStatus('${student.student_id}')">
                    <label for="student_${student.student_id}">
                        <div class="student-info">
                            <div class="student-name">${student.name}</div>
                            <div class="student-details">ID: ${student.student_id} | ${student.branch}-${student.section}</div>
                        </div>
                        <div class="student-status safe" id="status_${student.student_id}">SAFE</div>
                    </label>
                </div>
            `).join('')}
        </div>
    `;
    
    studentChecklist.innerHTML = checklistHTML;
}

// Select all students (mark as safe)
function selectAllStudents() {
    const checkboxes = document.querySelectorAll('#studentList input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
        updateStudentStatus(checkbox.value);
    });
}

// Deselect all students (mark as in danger)
function deselectAllStudents() {
    const checkboxes = document.querySelectorAll('#studentList input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
        updateStudentStatus(checkbox.value);
    });
}

// Update student status display
function updateStudentStatus(studentId) {
    const checkbox = document.getElementById(`student_${studentId}`);
    const statusElement = document.getElementById(`status_${studentId}`);
    
    if (checkbox.checked) {
        statusElement.textContent = 'SAFE';
        statusElement.className = 'student-status safe';
    } else {
        statusElement.textContent = 'IN DANGER';
        statusElement.className = 'student-status danger';
    }
}

// Get selected students (safe ones)
function getSelectedStudents() {
    const checkboxes = document.querySelectorAll('#studentList input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(checkbox => parseInt(checkbox.value));
}

// Trigger emergency alert
async function triggerEmergency(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const emergencyData = {
        emergency_type: formData.get('emergency_type'),
        emergency_message: formData.get('emergency_message'),
        branch: formData.get('branch'),
        section: formData.get('section'),
        selected_students: getSelectedStudents()  // Safe students (checked)
    };
    
    // Show loading overlay
    showLoadingOverlay();
    
    try {
        const response = await fetch('/api/emergency/trigger', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(emergencyData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage(`Emergency alert sent successfully! ${result.notifications_sent} notifications sent.`, 'success');
            
            // Reload status and activity
            await loadEmergencyStatus();
            await loadRecentActivity();
            
            // Reset form
            event.target.reset();
            toggleFilters();
        } else {
            showMessage(`Error: ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Error triggering emergency:', error);
        showMessage('Error triggering emergency alert', 'error');
    } finally {
        hideLoadingOverlay();
    }
}

// Quick emergency triggers
async function quickEmergency(type) {
    const messages = {
        fire: 'FIRE EMERGENCY: Evacuate immediately. Follow fire safety protocols.',
        medical: 'MEDICAL EMERGENCY: Medical assistance required. Stay calm and follow instructions.',
        weather: 'WEATHER ALERT: Severe weather conditions. Take appropriate shelter.',
        security: 'SECURITY ALERT: Security incident reported. Follow security protocols.'
    };
    
    const emergencyData = {
        emergency_type: 'all',
        emergency_message: messages[type]
    };
    
    showLoadingOverlay();
    
    try {
        const response = await fetch('/api/emergency/trigger', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(emergencyData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage(`${type.toUpperCase()} emergency alert sent! ${result.notifications_sent} notifications sent.`, 'success');
            
            // Reload status and activity
            await loadEmergencyStatus();
            await loadRecentActivity();
        } else {
            showMessage(`Error: ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Error triggering quick emergency:', error);
        showMessage('Error triggering emergency alert', 'error');
    } finally {
        hideLoadingOverlay();
    }
}

// Resolve emergency
async function resolveEmergency() {
    if (!confirm('Are you sure you want to resolve the current emergency?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/emergency/resolve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Emergency resolved successfully', 'success');
            
            // Reload status
            await loadEmergencyStatus();
        } else {
            showMessage(`Error: ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Error resolving emergency:', error);
        showMessage('Error resolving emergency', 'error');
    }
}

// View emergency details (for notifications page)
function viewEmergencyDetails(emergencyId) {
    // This would typically fetch detailed information about the emergency
    // For now, we'll show a simple modal
    const modal = document.getElementById('emergencyModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h3>Emergency Details</h3>
        <p><strong>Emergency ID:</strong> ${emergencyId}</p>
        <p>Detailed information about this emergency would be displayed here.</p>
        <p>This could include affected students, notification logs, timeline, etc.</p>
    `;
    
    modal.style.display = 'flex';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('emergencyModal');
    modal.style.display = 'none';
}

// Show loading overlay
function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

// Hide loading overlay
function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Show message
function showMessage(message, type = 'success') {
    const container = document.getElementById('messageContainer');
    if (!container) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    container.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.parentNode.removeChild(messageDiv);
        }
    }, 5000);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('emergencyModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Auto-refresh status every 30 seconds
setInterval(loadEmergencyStatus, 30000);

