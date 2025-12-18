"""
CORS preflight handler
"""
from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name='options', request_method='OPTIONS')
def options_handler(request):
    """Handle OPTIONS preflight requests"""
    response = Response(status=200)
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS, PATCH',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, Accept, Origin',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '86400'
    })
    return response
