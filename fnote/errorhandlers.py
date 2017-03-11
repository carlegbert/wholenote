from flask import jsonify, make_response


def register_errorhandlers(app):

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
