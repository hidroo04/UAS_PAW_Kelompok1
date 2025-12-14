"""
Booking Routes
Handles class booking management
"""

def includeme(config):
    """Configure booking routes"""
    
    # Booking management routes
    config.add_route('api_bookings', '/api/bookings')
    config.add_route('api_booking', '/api/bookings/{id}')
    config.add_route('api_my_bookings', '/api/bookings/my')
