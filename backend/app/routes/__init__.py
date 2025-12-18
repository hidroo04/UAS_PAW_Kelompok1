"""
Routes package - Modular route configuration
"""

def include_routes(config):
    """
    Include all route configurations
    """
    from . import auth_routes
    from . import class_routes
    from . import booking_routes
    from . import attendance_routes
    from . import membership_routes
    from . import review_routes
    from . import trainer_routes
    from . import user_routes
    from . import payment_routes
    
    # Include each route module
    auth_routes.includeme(config)
    class_routes.includeme(config)
    booking_routes.includeme(config)
    attendance_routes.includeme(config)
    membership_routes.includeme(config)
    review_routes.includeme(config)
    trainer_routes.includeme(config)
    user_routes.includeme(config)
    payment_routes.includeme(config)
