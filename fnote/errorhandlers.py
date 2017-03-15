from flask import jsonify, make_response


def register_errorhandlers(app):
    """Default error endpoints. These can be overriden for individual endpoints,
    eg, a login view might return a more specific message than just 'Forbidden'
    """

    @app.errorhandler(403)
    def forbidden(error):
        data = {'error': 'Forbidden', 'statusCode': 403}
        return make_response(jsonify(data), 403)

    @app.errorhandler(400)
    def bad_request(error):
        data = {'error': 'Bad request', 'statusCode': 401}
        return make_response(jsonify(data), 400)

    @app.errorhandler(405)
    def bad_method(error):
        data = {'error': 'Method not allowed',
                'statusCode': 405}
        return make_response(jsonify(data), 405)

    @app.errorhandler(404)
    def not_found(error):
        data = {'error': 'Not found',
                'statusCode': 404}
        return make_response(jsonify(data), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        data = {'error': 'Internal server error',
                'statusCode': 500}
        return make_response(jsonify(data), 500)
