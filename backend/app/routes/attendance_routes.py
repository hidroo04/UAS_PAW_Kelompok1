"""
Attendance Routes
Handles class attendance tracking
"""

def includeme(config):
    """Configure attendance routes"""
    
    # Attendance management routes
    config.add_route('api_attendance', '/api/attendance')
    config.add_route('api_my_attendance', '/api/attendance/my')
