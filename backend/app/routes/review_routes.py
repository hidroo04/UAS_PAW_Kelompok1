"""
Review Routes
Handles reviews and ratings for classes
"""

def includeme(config):
    """Configure review routes"""
    
    # Review routes
    config.add_route('api_class_reviews', '/api/classes/{id}/reviews')
    config.add_route('api_review', '/api/reviews/{id}')
    config.add_route('api_my_reviews', '/api/reviews/my')
