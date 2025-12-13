"""
Class Routes
Handles gym class management and scheduling
"""

def includeme(config):
    """Configure class routes"""
    
    # Class management routes
    config.add_route('api_classes', '/api/classes')
    config.add_route('api_class', '/api/classes/{id}')
    config.add_route('api_class_participants', '/api/classes/{id}/participants')
