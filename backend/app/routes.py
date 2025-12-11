def routes(config):
    """
    Define application routes
    """
    # Home
    config.add_route('home', '/')
    
    # User routes
    config.add_route('api_users', '/api/users')
    config.add_route('api_user', '/api/users/{id}')
    
    # Add more routes here
    # Example:
    # config.add_route('api_products', '/api/products')
    # config.add_route('api_product', '/api/products/{id}')
