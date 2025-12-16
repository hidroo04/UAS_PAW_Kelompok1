"""
Trainer Routes
Handles trainer-specific operations like managing class members
"""

def includeme(config):
    """Configure trainer routes"""
    
    # Trainer class management
    config.add_route('api_trainer_classes', '/api/trainer/classes')
    config.add_route('api_trainer_class_members', '/api/trainer/classes/{class_id}/members')
    config.add_route('api_trainer_remove_member', '/api/trainer/classes/{class_id}/members/{booking_id}')
    config.add_route('api_trainer_mark_attendance', '/api/trainer/classes/{class_id}/attendance/{booking_id}')
    
    # Trainer CRUD class operations
    config.add_route('api_trainer_create_class', '/api/trainer/classes/create')
    config.add_route('api_trainer_update_class', '/api/trainer/classes/{class_id}/update')
    config.add_route('api_trainer_delete_class', '/api/trainer/classes/{class_id}/delete')
