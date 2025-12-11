from pyramid.view import notfound_view_config, view_config


@notfound_view_config(renderer='json')
def notfound_view(request):
    request.response.status = 404
    return {'status': 'error', 'message': 'Not Found'}


@view_config(context=Exception, renderer='json')
def error_view(exc, request):
    request.response.status = 500
    return {'status': 'error', 'message': str(exc)}
