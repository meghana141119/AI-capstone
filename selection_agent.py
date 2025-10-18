import pandas as pd

class SelectionAgent:
    def __init__(self):
        self.role = 'Student Selection Specialist'
        self.goal = 'Filter and select students based on emergency criteria'
        self.backstory = 'You are an expert at quickly identifying and filtering student populations based on branch, section, or other criteria for emergency notifications.'
    
    def filter_students(self, students_data, filter_criteria):
        """
        Filter students based on the provided criteria
        
        Args:
            students_data: DataFrame containing student information
            filter_criteria: dict with filtering parameters
                - branch: specific branch to filter by
                - section: specific section to filter by
                - emergency_type: 'all', 'branch', or 'section'
                - selected_students: list of student IDs who are safe (checked)
        
        Returns:
            DataFrame: Filtered student data (students who need alerts - unchecked/safe ones)
        """
        filtered_students = students_data.copy()
        
        # First filter by branch/section
        if filter_criteria['emergency_type'] == 'all':
            # For 'all' type, we still need to filter by selected_students
            pass
        elif filter_criteria['emergency_type'] == 'branch':
            if 'branch' in filter_criteria:
                filtered_students = filtered_students[filtered_students['branch'] == filter_criteria['branch']]
                print(f"📋 FILTERING: {len(filtered_students)} students from {filter_criteria['branch']} branch")
        elif filter_criteria['emergency_type'] == 'section':
            if 'branch' in filter_criteria and 'section' in filter_criteria:
                filtered_students = filtered_students[
                    (filtered_students['branch'] == filter_criteria['branch']) &
                    (filtered_students['section'] == filter_criteria['section'])
                ]
                print(f"📋 FILTERING: {len(filtered_students)} students from {filter_criteria['branch']}-{filter_criteria['section']}")
        
        # Now filter out the selected (safe) students - we want to send alerts to the unchecked ones
        selected_students = filter_criteria.get('selected_students', [])
        if selected_students:
            # Convert selected_students to integers if they're strings
            selected_students = [int(sid) if isinstance(sid, str) else sid for sid in selected_students]
            # Keep only students who are NOT in the selected (safe) list
            filtered_students = filtered_students[~filtered_students['student_id'].isin(selected_students)]
            print(f"📋 AFFECTED: {len(filtered_students)} students need alerts (unchecked/in danger)")
            print(f"📋 SAFE: {len(selected_students)} students are safe (checked)")
        
        # Display affected students
        if not filtered_students.empty:
            print("Students needing alerts (unchecked/in danger):")
            for _, student in filtered_students.iterrows():
                print(f"  - {student['name']} ({student['student_id']}) - {student['branch']}-{student['section']}")
        else:
            print("✅ All students are safe - no alerts needed")
        
        return filtered_students
    
    def get_available_branches(self, students_data):
        """Get list of available branches"""
        return students_data['branch'].unique().tolist()
    
    def get_available_sections(self, students_data, branch=None):
        """Get list of available sections, optionally filtered by branch"""
        if branch:
            return students_data[students_data['branch'] == branch]['section'].unique().tolist()
        return students_data['section'].unique().tolist()
