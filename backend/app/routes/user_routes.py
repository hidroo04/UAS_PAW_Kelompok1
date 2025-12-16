"""
User/Profile routes
"""

def includeme(config):
    # Profile routes
    config.add_route('api_get_profile', '/api/profile')
    config.add_route('api_update_profile', '/api/profile/update')
    config.add_route('api_change_password', '/api/profile/change-password')
