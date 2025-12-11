"""
CORS preflight handler
"""
from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name='options', request_method='OPTIONS')
def options_handler(request):
    """Handle OPTIONS preflight requests"""
    response = Response()
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '3600'
    })
    return response
