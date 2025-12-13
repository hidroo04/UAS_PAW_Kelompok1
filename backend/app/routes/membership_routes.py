"""
Membership Routes
Handles membership plans and member management
"""

def includeme(config):
    """Configure membership routes"""
    
    # Membership management routes
    config.add_route('api_membership_plans', '/api/membership/plans')
    config.add_route('api_my_membership', '/api/membership/my')
    config.add_route('api_members', '/api/members')
