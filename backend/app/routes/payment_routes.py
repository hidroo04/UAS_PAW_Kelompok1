"""
Payment Routes
Handles payment gateway for membership
"""

def includeme(config):
    """Configure payment routes"""
    
    # Payment routes
    config.add_route('api_payment_create', '/api/payment/create')
    config.add_route('api_payment_all', '/api/payment/all')  # Admin: get all payments
    config.add_route('api_payment_report', '/api/payment/report')  # Admin: payment report with stats
    config.add_route('api_payment_status', '/api/payment/{order_id}/status')
    config.add_route('api_payment_callback', '/api/payment/callback')
    config.add_route('api_payment_history', '/api/payment/history')
    config.add_route('api_payment_methods', '/api/payment/methods')
    config.add_route('api_payment_simulate', '/api/payment/{order_id}/simulate')
